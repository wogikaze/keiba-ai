"""layout / parse の単体テスト。実データは使わず、合成した仕様書 CSV と行で確かめる。"""

import numpy as np
import polars as pl

from keiba_ai.jvdata.layout import check_layout, parse_format_csv
from keiba_ai.jvdata.parse import Batch
from keiba_ai.jvdata.tables import announced_at

# 仕様書「フォーマット」シートと同じ列の並び:
# 空, 項番, 副項番, キー, 項目名, 位置, 繰返, バイト, 合計, 初期値, 説明
SPEC = '''\
,９９．テスト,,,,レコード長,,33,バイト,,
,項番,,キー,項目名,位置,繰返,バイト,合計,初期値,説明
,1,,,レコード種別ID,1,,2,,,"""ZZ"" をセットレコードフォーマットを特定する"
,2,,,データ区分,3,,1,,0,
,3,,○,競馬場コード,4,,2,,0,
,,,,<見出しだけの行>,,,,,,
,4,,,本賞金,6,3,2,6,0,
,5,,,<オッズ>,12,3,6,18,,
,,a,,　　馬番,(   1),,2,,sp,
,,b,,　　オッズ,(   3),,4,,sp,
,6,,,符号付き,30,,2,,0,
,7,,,レコード区切,32,,2,,,CR/LF
'''


def test_layout_offsets():
    lay = parse_format_csv(SPEC)["ZZ"]
    assert lay.length == 31  # CR/LF を除く
    assert lay["競馬場コード"].start == 3
    assert lay["本賞金"].offsets() == [5, 7, 9]
    assert lay["オッズ.馬番"].offsets() == [11, 17, 23]
    assert lay["オッズ.オッズ"].offsets() == [13, 19, 25]
    assert "レコード区切" not in lay.fields
    assert check_layout(lay) == []


def _line(*parts: str) -> bytes:
    return "".join(parts).encode("cp932")


def test_batch_numbers_and_specials():
    lay = parse_format_csv(SPEC)["ZZ"]
    lines = [
        _line("ZZ", "1", "05", "01", " 2", "  ", "01", "0123", "02", "----", "03", "0000", "-5"),
        _line("ZZ", "7", "10", "99", "1 ", "**", "  ", "    ", "  ", "****", "  ", "9999", "+3"),
    ]
    b = Batch(lay, lines)
    assert b.bad_length == 0 and len(b) == 2
    assert b.str("競馬場コード").tolist() == ["05", "10"]
    prize = b.num("本賞金", None)
    assert prize[0, 0] == 1 and prize[0, 1] == 2  # 前の空白は右詰めとして読む
    assert np.isnan(prize[0, 2])  # すべて空白
    assert np.isnan(prize[1, 1])  # 数字の後の空白は不正
    assert np.isnan(prize[1, 2])  # 記号
    odds = b.num("オッズ.オッズ", None, 0.1)
    assert odds[0, 0] == 12.3 and np.isnan(odds[0, 1]) and odds[0, 2] == 0.0
    assert b.raw("オッズ.オッズ", None)[1].tolist() == [b"    ", b"****", b"9999"]
    assert b.num("符号付き", signed=True).tolist() == [-5.0, 3.0]


def test_text_decoding_and_bad_length():
    spec = SPEC.replace(",3,,○,競馬場コード,4,,2,,0,", ",3,,○,競馬場コード,4,,2,,Ｓ,")
    lay = parse_format_csv(spec)["ZZ"]
    line = "ZZ1".encode() + "馬".encode("cp932") + b"0" * 26
    b = Batch(lay, [line, b"ZZ1"])  # 2 行目は短い
    assert b.text("競馬場コード") == ["馬", ""]
    assert b.bad_length == 1


def test_announced_at_year_boundary():
    df = pl.DataFrame({
        "race_key": ["2024010606010101", "2024010606010101", "2023122806050911", "2024070101010101"],
        "announced_mdhm": ["12301000", "01060955", "01051200", "00000000"],
    })
    got = announced_at(df)["announced_at"].to_list()
    assert got[0].year == 2023 and got[0].month == 12  # 1 月のレースの 12 月の発売
    assert got[1].year == 2024
    assert got[2].year == 2024  # 12 月末のレースの 1 月の発表
    assert got[3] is None  # 発表時刻なし
