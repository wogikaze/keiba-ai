"""開催日の速報を、時刻つきで記録する（ポーリング版）。

計画（docs/data/jra-van-download-plan.md「週末: 速報の記録」）のうち、まずポーリングで取れるものを記録する。
JVWatchEvent によるイベント駆動（馬体重・払戻確定など）は未実装。

- 0B15（出走表）から当日のレース一覧と発走時刻を得る。
- 0B14（天候馬場・取消・変更）を --interval ごとに丸ごと取り直す。
- 各レースの全券種オッズ（--odds-spec、既定 0B30）を、発走 60 分前から 5 分おき、15 分前から 1 分おきに取る。
- 取得時刻をファイル名に付ける。

例:
  python jv_realtime.py 20261115
出力: raw\\realtime\\<dataspec>\\<YYYYMMDD>\\<key>_<取得時刻>.txt、ログは logs\\realtime_<YYYYMMDD>.jsonl
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time

import jvcommon as jc

# RA の発走時刻（JV-Data 仕様書「フォーマット」2. レース詳細の項目「発走時刻」）。
# 0 や空欄のときは発走時刻不明として、全レースを同じ間隔で取る。
RA_START_TIME_POS: int | None = 874  # 発走時刻 hhmm（仕様書 2. レース詳細 項番44）


def stamp() -> str:
    return dt.datetime.now().strftime("%H%M%S")


def record(jv, ds: str, key: str, date: str, log_path) -> dict:
    out = jc.RAW / "realtime" / ds / date / f"{key}_{stamp()}.txt"
    e = jc.rt_fetch(jv, ds, key, out)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def races_of_day(date: str) -> dict[str, dt.datetime | None]:
    """0B15 を取った最新ファイルから、当日のレース key と発走時刻を得る。"""
    d = jc.RAW / "realtime" / "0B15" / date
    files = sorted(d.glob(f"{date}_*.txt")) if d.exists() else []
    races: dict[str, dt.datetime | None] = {}
    if not files:
        return races
    with open(files[-1], "rb") as f:
        for line in f:
            if not line.startswith(b"RA"):
                continue
            key = line[11:27].decode("ascii")
            start = None
            if RA_START_TIME_POS:
                hhmm = line[RA_START_TIME_POS - 1:RA_START_TIME_POS + 3].decode("ascii", errors="replace")
                if hhmm.isdigit():
                    start = dt.datetime.strptime(date + hhmm, "%Y%m%d%H%M")
            races[key] = start
    return races


def due(start: dt.datetime | None, last: dt.datetime | None, now: dt.datetime, default_every: int) -> bool:
    if start is None:
        every = default_every
    else:
        to_post = (start - now).total_seconds() / 60
        if to_post > 60 or to_post < -5:
            return False
        every = 1 if to_post <= 15 else 5
    return last is None or (now - last).total_seconds() >= every * 60 - 5


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("date", help="YYYYMMDD")
    p.add_argument("--until", default="1730", help="この時刻（HHMM）で終わる")
    p.add_argument("--interval", type=int, default=5, help="0B14 と、発走時刻不明のレースのオッズの間隔（分）")
    p.add_argument("--odds-spec", default="0B30")
    p.add_argument("--once", action="store_true", help="1 巡だけ取って終わる（動作確認用）")
    a = p.parse_args()

    jc.setup_logging(f"realtime_{a.date}")
    jv = jc.open_jvlink()
    log_path = jc.LOGS / f"realtime_{a.date}.jsonl"
    end = dt.datetime.strptime(a.date + a.until, "%Y%m%d%H%M")
    record(jv, "0B15", a.date, a.date, log_path)
    races = races_of_day(a.date)
    jc.log.info("%s: %d レース", a.date, len(races))
    last_odds: dict[str, dt.datetime] = {}
    last_change: dt.datetime | None = None
    while True:
        now = dt.datetime.now()
        if last_change is None or (now - last_change).total_seconds() >= a.interval * 60:
            record(jv, "0B14", a.date, a.date, log_path)
            last_change = now
        for key, start in races.items():
            if due(start, last_odds.get(key), now, a.interval):
                record(jv, a.odds_spec, key, a.date, log_path)
                last_odds[key] = now
        if a.once or now >= end:
            break
        time.sleep(20)
    jc.log.info("終了: %s", a.date)


if __name__ == "__main__":
    main()
