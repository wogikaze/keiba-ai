"""JV-Link（JRA-VAN Data Lab.）から生レコードを取得するための共通部品。

Windows 上で実行する（JV-Link は Windows の COM 部品）。取得計画は docs/data/jra-van-download-plan.md。

- 読み出しは JVRead（JVGets は pywin32 でメモリが漏れる報告がある）。
- レコードは cp932 のバイト列として 1 行 1 レコードで保存する（固定長の位置がバイト単位のため）。
- 取得単位ごとにマニフェスト（JSON Lines）を追記し、再開時は済んだ単位を飛ばす。
- 環境変数 JV_FAKE=1 で偽の JV-Link（合成レコード）を使う。インストール前の動作確認用。
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(os.environ.get("JV_ROOT", r"E:\keiba-ai\jra-van"))
RAW = ROOT / "raw"
LOGS = ROOT / "logs"
MANIFEST = LOGS / "manifest.jsonl"
SAVE_PATH = ROOT / "jvlink-data"

PROGRESS_EVERY = 50_000
MAX_REOPEN = 3

log = logging.getLogger("jravan")


def setup_logging(name: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOGS / f"{name}_{stamp}.log", encoding="utf-8"),
    ]
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=handlers)


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- JV-Link


def open_jvlink(sid: str = "UNKNOWN"):
    """JV-Link の COM オブジェクトを作って JVInit する。JV_FAKE=1 なら偽物。"""
    if os.environ.get("JV_FAKE") == "1":
        from fake_jvlink import FakeJVLink

        jv = FakeJVLink()
    else:
        import win32com.client  # pywin32

        jv = win32com.client.Dispatch("JVDTLab.JVLink")
    ret = jv.JVInit(sid)
    if ret != 0:
        raise RuntimeError(f"JVInit が失敗: {ret}")
    return jv


def jv_open(jv, dataspec: str, fromtime: str, option: int) -> tuple[int, int, int, str]:
    """JVOpen。戻り値は (code, readcount, downloadcount, lastfiletimestamp)。"""
    ret = jv.JVOpen(dataspec, fromtime, option, 0, 0, "")
    if isinstance(ret, (list, tuple)):
        return int(ret[0]), int(ret[1] or 0), int(ret[2] or 0), str(ret[3] or "")
    return int(ret), 0, 0, ""


def wait_download(jv, downloadcount: int, timeout_s: float = 6 * 3600) -> None:
    """JVStatus でダウンロード完了を待つ。"""
    if downloadcount <= 0:
        return
    start = time.time()
    last = -1
    while True:
        st = int(jv.JVStatus())
        if st < 0:
            raise RuntimeError(f"JVStatus エラー: {st}")
        if st != last:
            log.info("download %d/%d", st, downloadcount)
            last = st
        if st >= downloadcount:
            return
        if time.time() - start > timeout_s:
            raise TimeoutError(f"ダウンロードが {timeout_s}s で終わらない ({st}/{downloadcount})")
        time.sleep(0.5)


@dataclass
class ReadResult:
    records: int = 0
    files: int = 0
    by_type: dict[str, int] = field(default_factory=dict)
    skipped: int = 0
    end_code: int = 0
    out_bytes: int = 0
    sha256: str = ""


class ReopenNeeded(Exception):
    """-402/-403（ファイル破損）や -502/-503 で、JVOpen からやり直す必要がある。"""

    def __init__(self, code: int, filename: str):
        super().__init__(f"JVRead {code} ({filename})")
        self.code = code
        self.filename = filename


def to_bytes(rec) -> bytes:
    """JVRead が返す文字列を cp932 のバイト列に戻し、末尾の改行と NUL を落とす。"""
    if isinstance(rec, (bytes, bytearray, memoryview)):
        b = bytes(rec)
    else:
        b = str(rec).encode("cp932", errors="replace")
    return b.rstrip(b"\r\n\x00")


def read_all(jv, out: Path, buffsize: int = 110_000) -> ReadResult:
    """JVRead で全レコードを読み、out に追記する。"""
    out.parent.mkdir(parents=True, exist_ok=True)
    res = ReadResult()
    h = hashlib.sha256()
    with open(out, "ab") as f:
        while True:
            ret = jv.JVRead("", buffsize, "")
            if isinstance(ret, (list, tuple)):
                code, buff, _size, fname = int(ret[0]), ret[1], ret[2], ret[3]
            else:  # 想定外の形
                raise RuntimeError(f"JVRead の戻り値が想定外: {ret!r}")
            if code > 0:
                b = to_bytes(buff)
                if not b:
                    res.skipped += 1
                    continue
                line = b + b"\n"
                f.write(line)
                h.update(line)
                res.out_bytes += len(line)
                res.records += 1
                rtype = b[:2].decode("ascii", errors="replace")
                res.by_type[rtype] = res.by_type.get(rtype, 0) + 1
                if res.records % PROGRESS_EVERY == 0:
                    log.info("read %d records (%s)", res.records, out.name)
            elif code == -1:
                res.files += 1
            elif code == 0:
                res.end_code = 0
                break
            elif code == -3:
                time.sleep(1)
            elif code in (-402, -403, -502, -503):
                raise ReopenNeeded(code, str(fname or ""))
            else:
                raise RuntimeError(f"JVRead エラー: {code} ({fname})")
    res.sha256 = h.hexdigest()
    return res


# ---------------------------------------------------------------- manifest


def manifest_done(kind: str, unit: str) -> bool:
    """マニフェストに、同じ kind・unit が status=ok で記録済みか。"""
    if not MANIFEST.exists():
        return False
    with open(MANIFEST, encoding="utf-8") as f:
        for line in f:
            try:
                m = json.loads(line)
            except json.JSONDecodeError:
                continue
            if m.get("kind") == kind and m.get("unit") == unit and m.get("status") == "ok":
                return True
    return False


def manifest_append(entry: dict) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch_unit(jv, kind: str, unit: str, dataspec: str, fromtime: str, option: int, out: Path) -> dict:
    """JVOpen → ダウンロード待ち → JVRead → JVClose を 1 単位として行い、マニフェストに記録する。

    out は書き始める前に消す（途中で落ちた単位の残りを持ち越さない）。
    """
    entry = {"kind": kind, "unit": unit, "dataspec": dataspec, "fromtime": fromtime, "option": option,
             "out": str(out), "started_at": now_iso()}
    for attempt in range(1, MAX_REOPEN + 1):
        out.unlink(missing_ok=True)
        code, readcount, downloadcount, lastts = jv_open(jv, dataspec, fromtime, option)
        entry.update(open_code=code, readcount=readcount, downloadcount=downloadcount, lastfiletimestamp=lastts,
                     attempt=attempt)
        if code == -1:
            jv.JVClose()
            # 該当データなし。「0 件で取得済み」とは扱わず、no_data として残す（計画の注意点）
            entry.update(status="no_data", finished_at=now_iso())
            manifest_append(entry)
            log.warning("%s %s: 該当データなし (-1)", kind, unit)
            return entry
        if code < 0:
            jv.JVClose()
            entry.update(status="error", finished_at=now_iso())
            manifest_append(entry)
            raise RuntimeError(f"JVOpen エラー {code}: {dataspec} {fromtime} option={option}")
        try:
            wait_download(jv, downloadcount)
            res = read_all(jv, out)
        except ReopenNeeded as e:
            jv.JVClose()
            log.warning("%s %s: %s。ファイルを消して開き直す (%d/%d)", kind, unit, e, attempt, MAX_REOPEN)
            if e.code in (-402, -403) and e.filename:
                jv.JVFiledelete(e.filename)
            continue
        jv.JVClose()
        entry.update(status="ok", records=res.records, files=res.files, by_type=res.by_type, skipped=res.skipped,
                     bytes=res.out_bytes, sha256=res.sha256, finished_at=now_iso())
        manifest_append(entry)
        log.info("%s %s: %d records %s", kind, unit, res.records, res.by_type)
        return entry
    entry.update(status="error", finished_at=now_iso())
    manifest_append(entry)
    raise RuntimeError(f"{kind} {unit}: {MAX_REOPEN} 回開き直しても読めなかった")


def rt_fetch(jv, dataspec: str, key: str, out: Path) -> dict:
    """速報系（JVRTOpen）を 1 key 取得する。"""
    out.unlink(missing_ok=True)
    code = int(jv.JVRTOpen(dataspec, key))
    entry = {"dataspec": dataspec, "key": key, "open_code": code, "out": str(out), "fetched_at": now_iso()}
    if code == -1:
        jv.JVClose()
        entry["status"] = "no_data"
        return entry
    if code < 0:
        jv.JVClose()
        entry["status"] = "error"
        return entry
    try:
        res = read_all(jv, out)
    except ReopenNeeded as e:
        jv.JVClose()
        entry.update(status="error", read_code=e.code)
        return entry
    jv.JVClose()
    entry.update(status="ok", records=res.records, by_type=res.by_type, bytes=res.out_bytes, sha256=res.sha256)
    return entry
