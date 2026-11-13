"""JV-Link をインストールした直後の動作確認（Day 0）。

1. JVInit → 保存パスと保存フラグを設定する（JVSetSavePath / JVSetSaveFlag）
2. 直近 7 日の RACE を option 1 で開き、レコード種別ごとの件数を数える
3. 直近の JRA のレース 1 つについて 0B41・0B42 を JVRTOpen し、発表月日時分の一覧（オッズの刻み）を出す

結果は logs\\smoke_<日時>.json に保存する。
"""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter

import jvcommon as jc


def main() -> None:
    jc.setup_logging("smoke")
    jv = jc.open_jvlink()
    result: dict = {"at": jc.now_iso()}
    jc.SAVE_PATH.mkdir(parents=True, exist_ok=True)
    result["JVSetSavePath"] = jv.JVSetSavePath(str(jc.SAVE_PATH))
    result["JVSetSaveFlag"] = jv.JVSetSaveFlag(1)

    since = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y%m%d000000")
    out = jc.RAW / "_smoke" / "RACE_7days.txt"
    e = jc.fetch_unit(jv, "smoke", f"RACE:{since}:{dt.datetime.now():%H%M%S}", "RACE", since, 1, out)
    result["race_open"] = {k: e.get(k) for k in ("status", "open_code", "readcount", "downloadcount", "records", "by_type")}

    keys = []
    if out.exists():
        with open(out, "rb") as f:
            for line in f:
                if line.startswith(b"RA") and line[19:21].decode("ascii", "replace") in {f"{i:02d}" for i in range(1, 11)}:
                    keys.append(line[11:27].decode("ascii"))
    keys = sorted(set(keys))
    result["jra_races_in_7days"] = len(keys)
    yesterday = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y%m%d")
    past = [k for k in keys if k[:8] <= yesterday]
    if past:
        key = past[-1]
        result["timeseries_key"] = key
        for ds in ("0B41", "0B42"):
            o = jc.RAW / "_smoke" / f"{ds}_{key}.txt"
            r = jc.rt_fetch(jv, ds, key, o)
            times: Counter = Counter()
            if o.exists():
                for line in open(o, "rb"):
                    # O1/O2 の発表月日時分は 28 バイト目から 8 バイト（mmddhhmm）
                    times[line[27:35].decode("ascii", "replace")] += 1
            result[ds] = {"status": r.get("status"), "open_code": r.get("open_code"), "records": r.get("records"),
                          "announce_times": sorted(times)}
    path = jc.LOGS / f"smoke_{dt.datetime.now():%Y%m%d-%H%M%S}.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
