"""セットアップ（option 4）を dataspec × 年で取得する。

例:
  python jv_setup.py RACE 1986 2026     # 1 年ずつ。今年は今の時刻までで区切る
  python jv_setup.py DIFN --all         # 期間指定できない種別は 1 回で取る

出力: raw\\<dataspec>\\<年>.txt（--all のときは raw\\<dataspec>\\all.txt）。
最後に返った lastfiletimestamp を logs\\state_<dataspec>.json に保存する（以後の差分取得の起点）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json

import jvcommon as jc


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("dataspec")
    p.add_argument("start", nargs="?", type=int)
    p.add_argument("end", nargs="?", type=int)
    p.add_argument("--all", action="store_true", help="期間指定せずに 1 回で取る（DIFN、BLDN、HOSN など）")
    p.add_argument("--from", dest="from_", default="19860101000000", help="--all のときの fromtime")
    p.add_argument("--option", type=int, default=4, help="4: セットアップ（ダイアログなし）、3: セットアップ、1: 通常")
    a = p.parse_args()

    jc.setup_logging(f"setup_{a.dataspec}")
    jv = jc.open_jvlink()
    last_ts = ""
    if a.all:
        unit = f"all:{a.from_}"
        if jc.manifest_done("setup", f"{a.dataspec}:{unit}"):
            jc.log.info("済み: %s %s", a.dataspec, unit)
            return
        e = jc.fetch_unit(jv, "setup", f"{a.dataspec}:{unit}", a.dataspec, a.from_, a.option,
                          jc.RAW / a.dataspec / "all.txt")
        last_ts = e.get("lastfiletimestamp", "")
    else:
        if a.start is None:
            p.error("start 年か --all を指定する")
        end = a.end or dt.date.today().year
        for year in range(a.start, end + 1):
            begin = f"{year}0101000000"
            # 開発ガイド p.23 は「最後の 1 回は終了時刻を付けない」とするが、お試し中の RACE は
            # 終了時刻なしの option 4 で -301（認証エラー）になった（2026-11-13）。最後の年は今の時刻で区切り、
            # それ以降は jv_update.py（option 1）で差分を取る
            stop = dt.datetime.now().strftime("%Y%m%d%H%M%S") if year == dt.date.today().year else f"{year + 1}0101000000"
            fromtime = f"{begin}-{stop}"
            unit = f"{a.dataspec}:{year}"
            if jc.manifest_done("setup", unit):
                jc.log.info("済み: %s", unit)
                continue
            e = jc.fetch_unit(jv, "setup", unit, a.dataspec, fromtime, a.option,
                              jc.RAW / a.dataspec / f"{year}.txt")
            last_ts = e.get("lastfiletimestamp", "") or last_ts
    if last_ts:
        state = jc.LOGS / f"state_{a.dataspec}.json"
        state.write_text(json.dumps({"dataspec": a.dataspec, "lastfiletimestamp": last_ts, "updated_at": jc.now_iso()},
                                    ensure_ascii=False), encoding="utf-8")
        jc.log.info("state: %s = %s", a.dataspec, last_ts)


if __name__ == "__main__":
    main()
