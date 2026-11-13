"""テスト用の偽 JV-Link。JVOpen・JVStatus・JVRead・JVRTOpen・JVClose などの戻り値を真似る。

本物の JV-Link をインストールする前に、取得スクリプトの流れ（再試行、マニフェスト、出力）を確かめるために使う。
レコードは合成したもので、実際のデータは含まない。
"""

from __future__ import annotations

import os


def _ra(year: int, mmdd: str, jyo: str, kai: int, nichi: int, race: int, kubun: str = "7") -> str:
    # RA の先頭 27 バイト: 種別(2) データ区分(1) 作成日(8) 開催年(4) 月日(4) 競馬場(2) 回(2) 日目(2) R(2)
    head = f"RA{kubun}{year}0101{year}{mmdd}{jyo}{kai:02d}{nichi:02d}{race:02d}"
    return head.ljust(1272, " ")


def _se(year: int, mmdd: str, jyo: str, race: int, umaban: int) -> str:
    return f"SE7{year}0101{year}{mmdd}{jyo}0101{race:02d}{umaban:02d}".ljust(555, " ")


def _o1(key: str, hhmm: str) -> str:
    # O1 の発表月日時分は 28 バイト目から 8 バイト（mmddhhmm）
    return f"O13{key[:8]}{key}{key[4:8]}{hhmm}".ljust(962, " ")


class FakeJVLink:
    def __init__(self) -> None:
        self._queue: list[object] = []
        self._fail_once = os.environ.get("JV_FAKE_FAIL_ONCE") == "1"

    # 設定系 -----------------------------------------------------------
    def JVInit(self, sid: str) -> int:
        return 0

    def JVSetUIProperties(self) -> int:
        return 0

    def JVSetSavePath(self, path: str) -> int:
        return 0

    def JVSetSaveFlag(self, flag: int) -> int:
        return 0

    def JVSetServiceKey(self, key: str) -> int:
        return 0

    def JVFiledelete(self, filename: str) -> int:
        return 0

    # 蓄積系 -----------------------------------------------------------
    def JVOpen(self, dataspec: str, fromtime: str, option: int, readcount, downloadcount, lastts):
        year = int(fromtime[:4])
        if dataspec == "NONE":
            return (-1, 0, 0, "")
        recs: list[object] = []
        if dataspec == "RACE":
            for race in range(1, 4):
                recs.append(_ra(year, "0105", "06", 1, 1, race))
                for umaban in range(1, 4):
                    recs.append(_se(year, "0105", "06", race, umaban))
            recs.append(_ra(year, "0105", "A4", 1, 1, 1, kubun="A"))  # 地方（除外される）
        else:
            recs.append(f"{dataspec[:2]}1{year}0101".ljust(100, " "))
        # 2 ファイルに分けたことにする（-1 = ファイル切替）
        half = len(recs) // 2
        self._queue = recs[:half] + [-1] + recs[half:] + [-1]
        if self._fail_once:
            self._fail_once = False
            self._queue.insert(1, -402)
        return (0, 2, 2, f"{year}1231235959")

    def JVStatus(self) -> int:
        return 2

    def JVRead(self, buff, size, filename):
        if not self._queue:
            return (0, "", 0, "")
        item = self._queue.pop(0)
        if isinstance(item, int):
            return (item, "", 0, "FAKE.dat")
        return (len(item), item + "\r\n", len(item), "FAKE.dat")

    def JVClose(self) -> int:
        self._queue = []
        return 0

    # 速報系 -----------------------------------------------------------
    def JVRTOpen(self, dataspec: str, key: str) -> int:
        if dataspec == "0B15":
            # 当日のレース一覧。発走時刻（874 バイト目から hhmm）を今から 10 分後・90 分後にする
            import datetime as dt

            recs = []
            for race, mins in ((1, 10), (2, 90)):
                hhmm = (dt.datetime.now() + dt.timedelta(minutes=mins)).strftime("%H%M")
                ra = _ra(int(key[:4]), key[4:8], "06", 1, 1, race)
                recs.append(ra[:873] + hhmm + ra[877:])
            self._queue = recs
            return 0
        if dataspec in ("0B41", "0B42"):
            self._queue = [_o1(key, hhmm) for hhmm in ("0930", "1000", "1030")]
        else:
            self._queue = [f"{dataspec}{key}".ljust(200, " ")]
        return 0
