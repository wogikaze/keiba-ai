"""時系列オッズ（0B41: 単複枠、0B42: 馬連）を、レースごとに JVRTOpen で取得する。

レースの key は、セットアップで取った RA（raw\\RACE\\<年>.txt）から作る。
JRA の競馬場（コード 01〜10）だけを対象にし、新しい年から古い年へ進む。
同じ key は 1 回だけ開く（2 回目以降に古い版が返る報告がある: jrvltsql #288）。

例:
  python jv_timeseries.py 2026 2003            # 2026 年から 2003 年へ
  python jv_timeseries.py 2025 2025 --since 20251113   # 指定日以降だけ
出力: raw\\0B41\\<年>\\<key>.txt、raw\\0B42\\<年>\\<key>.txt。結果は logs\\timeseries_<年>.jsonl。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json

import jvcommon as jc

JRA_JYO = {f"{i:02d}" for i in range(1, 11)}
# RA のバイト位置（1 始まり、JV-Data 仕様書「フォーマット」2. レース詳細）
#   開催年 12-15、開催月日 16-19、競馬場 20-21、開催回 22-23、開催日目 24-25、レース番号 26-27
KEY_SLICE = slice(11, 27)
JYO_SLICE = slice(19, 21)
KUBUN_POS = 2  # データ区分（3 バイト目）。0: 削除、9: 中止


def race_keys(year: int) -> list[str]:
    path = jc.RAW / "RACE" / f"{year}.txt"
    if not path.exists():
        raise FileNotFoundError(f"{path} が無い。先に jv_setup.py RACE で取得する")
    keys: set[str] = set()
    with open(path, "rb") as f:
        for line in f:
            if not line.startswith(b"RA"):
                continue
            if line[KUBUN_POS:KUBUN_POS + 1] == b"0":
                continue
            if line[JYO_SLICE].decode("ascii", errors="replace") not in JRA_JYO:
                continue
            keys.add(line[KEY_SLICE].decode("ascii"))
    return sorted(keys, reverse=True)


def done_keys(year: int) -> set[tuple[str, str]]:
    path = jc.LOGS / f"timeseries_{year}.jsonl"
    done: set[tuple[str, str]] = set()
    if path.exists():
        for line in open(path, encoding="utf-8"):
            m = json.loads(line)
            # no_data も「開いた」ので再度は開かない（同じ key を何度も開かない方針）
            if m.get("status") in ("ok", "no_data"):
                done.add((m["dataspec"], m["key"]))
    return done


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("start", type=int, help="新しい方の年")
    p.add_argument("end", type=int, help="古い方の年")
    p.add_argument("--since", help="この日（YYYYMMDD）以降のレースだけ")
    p.add_argument("--until", help="この日（YYYYMMDD）以前のレースだけ。既定は昨日")
    p.add_argument("--specs", default="0B41,0B42")
    p.add_argument("--stop-after-nodata", type=int, default=200,
                   help="連続でこの件数だけ no_data が続いたら、その年を打ち切る")
    a = p.parse_args()

    jc.setup_logging("timeseries")
    jv = jc.open_jvlink()
    specs = a.specs.split(",")
    until = a.until or (dt.date.today() - dt.timedelta(days=1)).strftime("%Y%m%d")
    for year in range(a.start, a.end - 1, -1):
        keys = [k for k in race_keys(year) if k[:8] <= until and (not a.since or k[:8] >= a.since)]
        done = done_keys(year)
        log_path = jc.LOGS / f"timeseries_{year}.jsonl"
        ok = nodata = streak = 0
        jc.log.info("%d 年: %d レース（済み %d 件）", year, len(keys), len(done))
        for i, key in enumerate(keys, 1):
            for ds in specs:
                if (ds, key) in done:
                    continue
                e = jc.rt_fetch(jv, ds, key, jc.RAW / ds / str(year) / f"{key}.txt")
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
                if e["status"] == "ok":
                    ok += 1
                    streak = 0
                elif e["status"] == "no_data":
                    nodata += 1
                    streak += 1
                else:
                    jc.log.warning("error %s %s: %s", ds, key, e)
            if i % 200 == 0:
                jc.log.info("%d 年: %d/%d レース（ok %d, no_data %d）", year, i, len(keys), ok, nodata)
            if streak >= a.stop_after_nodata:
                jc.log.warning("%d 年: no_data が %d 件続いたので打ち切る", year, streak)
                break
        jc.manifest_append({"kind": "timeseries", "unit": str(year), "races": len(keys), "ok": ok,
                            "no_data": nodata, "status": "ok", "finished_at": jc.now_iso()})
        jc.log.info("%d 年: 完了 ok %d, no_data %d / %d レース", year, ok, nodata, len(keys))


if __name__ == "__main__":
    main()
