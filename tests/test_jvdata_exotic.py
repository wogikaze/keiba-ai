"""O2〜O6（馬連〜3連単）の変換と、0B42 のスナップショットの選び方の単体テスト。

実データと本物の仕様書は使わず、項目名だけ仕様書に合わせた小さいレイアウトで確かめる。
"""

from datetime import datetime

import numpy as np
import polars as pl

from keiba_ai.jvdata.build import select_snapshots
from keiba_ai.jvdata.layout import check_layout, parse_format_csv
from keiba_ai.jvdata.parse import Batch
from keiba_ai.jvdata.tables import latest, parse_exotic

_HEAD = '''\
,{title},,,,レコード長,,{length},バイト,,
,項番,,キー,項目名,位置,繰返,バイト,合計,初期値,説明
,1,,,レコード種別ID,1,,2,,,"""{rid}"" をセットレコードフォーマットを特定する"
,2,,,データ区分,3,,1,,0,
,3,,,データ作成年月日,4,,8,,0,
,4,,○,開催年,12,,4,,0,
,5,,○,開催月日,16,,4,,0,
,6,,○,競馬場コード,20,,2,,0,
,7,,○,開催回[第N回],22,,2,,0,
,8,,○,開催日目[N日目],24,,2,,0,
,9,,○,レース番号,26,,2,,0,
,10,,,発表月日時分,28,,8,,0,
,11,,,登録頭数,36,,2,,0,
,12,,,出走頭数,38,,2,,0,
,13,,,発売フラグ　{name},40,,1,,0,
'''

# 馬連は 3 組、3連単は 2 組だけの縮小版（本物は 153 組・4,896 組）
SPEC = _HEAD.format(title="オッズ2", length=40 + 3 * 13 + 11 + 2, rid="O2", name="馬連") + '''\
,14,,,<馬連オッズ>,41,3,13,39,,
,,a,,　　組番,(   1),,4,,sp,
,,b,,　　オッズ,(   5),,6,,sp,
,,c,,　　人気順,(  11),,3,,sp,
,15,,,馬連票数合計,80,,11,,sp,
,16,,,レコード区切,91,,2,,,CR/LF
''' + _HEAD.format(title="オッズ6", length=40 + 2 * 17 + 11 + 2, rid="O6", name="3連単") + '''\
,14,,,<3連単オッズ>,41,2,17,34,,
,,a,,　　組番,(   1),,6,,sp,
,,b,,　　オッズ,(   7),,7,,sp,
,,c,,　　人気順,(  14),,4,,sp,
,15,,,3連単票数合計,75,,11,,sp,
,16,,,レコード区切,86,,2,,,CR/LF
'''

KEY = "2024010606010101"


def _rec(rid: str, kubun: str, created: str, mdhm: str, combos: list[str], total: str) -> bytes:
    return (rid + kubun + created + KEY + mdhm + "1614" + "7" + "".join(combos) + total).encode()


def test_layouts():
    lays = parse_format_csv(SPEC)
    assert check_layout(lays["O2"]) == [] and check_layout(lays["O6"]) == []


def test_parse_quinella_specials_and_blank():
    lay = parse_format_csv(SPEC)["O2"]
    line = _rec("O2", "5", "20240109", "00000000",
                ["0102" + "000123" + "  1", "0103" + "------" + "---", "    " + "      " + "   "],
                "00000012345")
    df = parse_exotic(Batch(lay, [line]), "O2", np.array([7]))
    assert df.height == 2  # 空白の組番は落とす
    assert df["combination"].to_list() == ["0102", "0103"]
    assert df["a"].to_list() == [1, 1] and df["b"].to_list() == [2, 3]
    assert df["odds"].to_list() == [12.3, None]
    assert df["pop"].to_list() == [1, None]
    assert df["status"].cast(pl.String).to_list() == ["ok", "cancel_pre"]
    assert df["vote_total"].to_list() == [1234500, 1234500]  # 百円 → 円
    assert df["race_key"].to_list() == [KEY, KEY]
    assert df["_order"].to_list() == [7, 7]


def test_parse_trifecta_wide_odds_field():
    lay = parse_format_csv(SPEC)["O6"]
    line = _rec("O6", "5", "20240109", "00000000",
                ["050711" + "1234567" + "4896", "110705" + "0000000" + "4896"], "00000000001")
    df = parse_exotic(Batch(lay, [line]), "O6", np.array([0]))
    assert df.select("a", "b", "c").rows() == [(5, 7, 11), (11, 7, 5)]  # 着順の順
    assert df["odds"].to_list() == [123456.7, None]  # 7 桁
    assert df["status"].cast(pl.String).to_list() == ["ok", "no_vote"]
    assert df["pop"].to_list() == [4896, None]


def test_latest_record_per_race():
    lay = parse_format_csv(SPEC)["O2"]
    combos = ["0102" + "000123" + "  1"] + ["    " + " " * 9] * 2
    lines = [
        _rec("O2", "4", "20240106", "00000000", combos, "00000000001"),
        _rec("O2", "5", "20240109", "00000000", combos, "00000000002"),
    ]
    b = Batch(lay, lines)
    df = parse_exotic(b, "O2", np.arange(2))
    meta = df.select("race_key", "data_kubun", "created_date", "_rank", "_order").unique()
    best = latest(meta, ["race_key"])
    assert best["data_kubun"].to_list() == ["5"]


def test_select_snapshots():
    post = datetime(2024, 1, 6, 10, 10)
    t = lambda h, m: datetime(2024, 1, 6, h, m)  # noqa: E731
    rec = pl.DataFrame({
        "i": [0, 1, 2, 3, 4],
        "race_key": [KEY] * 5,
        "data_kubun": ["1", "1", "1", "1", "4"],
        "announced_at": [t(9, 0), t(9, 58), t(10, 4), t(10, 12), t(10, 15)],
        "post_at": [post] * 5,
    })
    sel = select_snapshots(rec, minutes=(1, 5, 10, 30, 60))
    got = dict(zip(sel["snap"], sel["i"]))
    # 発走 10:10。1 分前・5 分前は 10:04、10 分前は 9:58、30・60 分前は 9:00。
    # 発走後の中間（10:12）は N 分前には使わない。last は確定（10:15）
    assert got == {"1": 2, "5": 2, "10": 1, "30": 0, "60": 0, "last": 4}


def test_select_snapshots_no_early_announcement():
    rec = pl.DataFrame({
        "i": [0], "race_key": [KEY], "data_kubun": ["1"],
        "announced_at": [datetime(2024, 1, 6, 10, 8)], "post_at": [datetime(2024, 1, 6, 10, 10)],
    })
    sel = select_snapshots(rec, minutes=(1, 5))
    assert sel.sort("snap")["snap"].to_list() == ["1", "last"]  # 5 分前の発表はないので行もない
