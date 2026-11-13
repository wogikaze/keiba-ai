"""通常データ（option 1）の差分を取得する。

前回の lastfiletimestamp（logs\\state_<dataspec>.json）を fromtime にして開き、
返った lastfiletimestamp で state を更新する。

例:
  python jv_update.py RACE DIFN BLDN SNPN SLOP WOOD YSCH HOSN HOYU MING COMM TOKU
"""

from __future__ import annotations

import argparse
import datetime as dt
import json

import jvcommon as jc


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("dataspecs", nargs="+")
    p.add_argument("--default-from", default=None, help="state が無いときの fromtime（既定: 1 年前）")
    a = p.parse_args()

    jc.setup_logging("update")
    jv = jc.open_jvlink()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for ds in a.dataspecs:
        state = jc.LOGS / f"state_{ds}.json"
        if state.exists():
            fromtime = json.loads(state.read_text(encoding="utf-8"))["lastfiletimestamp"]
        else:
            fromtime = a.default_from or (dt.date.today() - dt.timedelta(days=365)).strftime("%Y%m%d000000")
            jc.log.warning("%s: state が無いので %s から", ds, fromtime)
        try:
            e = jc.fetch_unit(jv, "update", f"{ds}:{stamp}", ds, fromtime, 1, jc.RAW / ds / "update" / f"{stamp}.txt")
        except RuntimeError as err:
            # 1 種別の失敗で残りを止めない。state は進めないので次回また同じ fromtime から取る
            jc.log.error("%s: %s", ds, err)
            continue
        if e.get("status") == "ok" and e.get("lastfiletimestamp"):
            state.write_text(json.dumps({"dataspec": ds, "lastfiletimestamp": e["lastfiletimestamp"],
                                         "updated_at": jc.now_iso()}, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
