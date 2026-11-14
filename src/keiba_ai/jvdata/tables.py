"""レコード種別ごとの変換（Batch → polars DataFrame）と、版の重複除去。

列名は英語の snake_case。仕様書の項目名との対応は docs/data/processed.md に書く。
単位の換算（0.1 倍など）はここで済ませる。数字として読めない値はすべて null。
"""

from __future__ import annotations

import numpy as np
import polars as pl

from .parse import Batch

JRA_VENUES = {f"{i:02d}" for i in range(1, 11)}

# 版の新しさ。同じ作成日なら値が大きい方を採る。0（削除）は同日なら最優先。
KUBUN_RANK = {
    "RA": {**{str(i): i for i in range(1, 8)}, "9": 8, "0": 9},
    "SE": {**{str(i): i for i in range(1, 8)}, "9": 8, "0": 9},
    "HR": {"1": 1, "2": 2, "9": 3, "0": 4},
    **{t: {**{str(i): i for i in range(1, 6)}, "9": 6, "0": 7} for t in ("O1", "O2", "O3", "O4", "O5", "O6")},
}

ODDS_STATUS = pl.Enum(["ok", "no_vote", "cancel_pre", "cancel_post"])
_STATUS_CODE = {b"0000": "no_vote", b"----": "cancel_pre", b"****": "cancel_post"}


def _ser(name: str, a, dtype=None) -> pl.Series:
    if isinstance(a, np.ndarray) and a.dtype.kind == "f":
        s = pl.Series(name, a, nan_to_null=True)
        return s.cast(dtype) if dtype is not None else s
    s = pl.Series(name, a)
    return s.cast(dtype) if dtype is not None else s


def _empty_to_null(s: pl.Series) -> pl.Series:
    return s.replace("", None) if s.dtype == pl.String else s


def _date(b: Batch, name: str, i: int = 0) -> pl.Series:
    return _ser("d", b.str(name, i)).str.strptime(pl.Date, "%Y%m%d", strict=False)


def race_key(b: Batch) -> np.ndarray:
    """開催年〜レース番号の 16 桁（年月日場回日R）。仕様書上この 6 項目は連続している。"""
    f0, f1 = b.layout["開催年"], b.layout["レース番号"]
    assert f1.start + f1.length - f0.start == 16
    a = np.ascontiguousarray(b.mat[:, f0.start : f0.start + 16])
    return np.char.decode(a.view("S16").ravel(), "ascii", errors="replace")


def header(b: Batch, rtype: str, order: np.ndarray) -> dict[str, pl.Series]:
    kubun = b.str("データ区分")
    rank = KUBUN_RANK.get(rtype, {})
    return {
        "data_kubun": _ser("data_kubun", kubun),
        "created_date": _date(b, "データ作成年月日"),
        "_rank": _ser("_rank", np.array([rank.get(k, 0) for k in kubun.tolist()], dtype=np.int8)),
        "_order": _ser("_order", order.astype(np.int64)),
    }


def jra_rows(b: Batch) -> np.ndarray:
    return np.isin(b.str("競馬場コード"), list(JRA_VENUES))


def latest(df: pl.DataFrame, keys: list[str]) -> pl.DataFrame:
    """キーごとに最新の版を 1 行残す（作成日 → データ区分の順位 → 読んだ順）。最新が削除なら消す。"""
    df = df.sort(["created_date", "_rank", "_order"], nulls_last=False, maintain_order=True)
    df = df.unique(subset=keys, keep="last", maintain_order=True)
    return df.filter(pl.col("data_kubun") != "0").drop(["_rank", "_order"])


# ---------------------------------------------------------------- RA レース詳細


def parse_ra(b: Batch, order: np.ndarray) -> pl.DataFrame:
    key = race_key(b)
    n = lambda name, scale=1.0, dt=pl.Int32: _ser(name, b.num(name, 0, scale), dt)  # noqa: E731
    track = b.str("トラックコード")
    surface = np.select(
        [(track >= "10") & (track <= "22"), (track >= "23") & (track <= "29"), (track >= "51") & (track <= "59")],
        ["turf", "dirt", "jump"],
        default="",
    )
    post = b.str("発走時刻")
    cols = {
        "race_key": _ser("race_key", key),
        "date": _ser("date", np.char.add(b.str("開催年"), b.str("開催月日"))).str.strptime(pl.Date, "%Y%m%d", strict=False),
        "venue_code": _ser("venue_code", b.str("競馬場コード")),
        "kai": n("開催回[第N回]", dt=pl.Int16),
        "nichi": n("開催日目[N日目]", dt=pl.Int16),
        "race_no": n("レース番号", dt=pl.Int16),
        "weekday_code": _ser("weekday_code", b.str("曜日コード")),
        "special_race_no": n("特別競走番号"),
        "race_name": _ser("race_name", b.text("競走名本題")),
        "race_subname": _ser("race_subname", b.text("競走名副題")),
        "race_name_paren": _ser("race_name_paren", b.text("競走名カッコ内")),
        "race_name_short": _ser("race_name_short", b.text("競走名略称10文字")),
        "grade_code": _ser("grade_code", b.str("グレードコード")),
        "race_type_code": _ser("race_type_code", b.str("競走種別コード")),
        "race_symbol_code": _ser("race_symbol_code", b.str("競走記号コード")),
        "weight_type_code": _ser("weight_type_code", b.str("重量種別コード")),
        "cond_2yo": _ser("cond_2yo", b.str("競走条件コード2歳条件")),
        "cond_3yo": _ser("cond_3yo", b.str("競走条件コード3歳条件")),
        "cond_4yo": _ser("cond_4yo", b.str("競走条件コード4歳条件")),
        "cond_5up": _ser("cond_5up", b.str("競走条件コード5歳以上条件")),
        "cond_youngest": _ser("cond_youngest", b.str("競走条件コード最若年条件")),
        "distance": n("距離", dt=pl.Int16),
        "track_code": _ser("track_code", track),
        "surface": _ser("surface", surface),
        "course_kubun": _ser("course_kubun", b.str("コース区分")),
        "prize_1st": _ser("prize_1st", b.num("本賞金", 0, 100.0), pl.Int64),
        "post_time": _ser("post_time", post),
        "n_registered": n("登録頭数", dt=pl.Int16),
        "n_starters": n("出走頭数", dt=pl.Int16),
        "n_finishers": n("入線頭数", dt=pl.Int16),
        "weather_code": _ser("weather_code", b.str("天候コード")),
        "turf_going_code": _ser("turf_going_code", b.str("芝馬場状態コード")),
        "dirt_going_code": _ser("dirt_going_code", b.str("ダート馬場状態コード")),
        "first_3f": n("前3ハロン", 0.1, pl.Float64),
        "first_4f": n("前4ハロン", 0.1, pl.Float64),
        "last_3f": n("後3ハロン", 0.1, pl.Float64),
        "last_4f": n("後4ハロン", 0.1, pl.Float64),
        "record_flag": _ser("record_flag", b.str("レコード更新区分")),
    }
    df = pl.DataFrame({**cols, **header(b, "RA", order)})
    df = df.with_columns(
        [_empty_to_null(df[c]) for c in df.columns if df[c].dtype == pl.String],
    )
    for c in ("first_3f", "first_4f", "last_3f", "last_4f", "distance", "n_starters", "n_finishers"):
        df = df.with_columns(pl.when(pl.col(c) == 0).then(None).otherwise(pl.col(c)).alias(c))
    post_at = (pl.col("date").dt.strftime("%Y%m%d") + pl.col("post_time")).str.strptime(
        pl.Datetime("us"), "%Y%m%d%H%M", strict=False
    )
    going = (
        pl.when(pl.col("surface") == "dirt")
        .then(pl.col("dirt_going_code"))
        .otherwise(pl.col("turf_going_code"))
    )
    return df.with_columns(
        post_at=post_at,
        post_time=pl.when(pl.col("post_time") == "0000").then(None).otherwise(pl.col("post_time")),
        going_code=going,
        year=pl.col("date").dt.year().cast(pl.Int16),
    )


# ---------------------------------------------------------------- SE 馬毎レース情報


def _race_time(b: Batch, name: str) -> np.ndarray:
    """走破タイム 'mss.s'（4 桁、例 1234 = 1分23秒4）を秒に。0 は欠損。"""
    v = b.num(name)
    sec = np.floor(v / 1000) * 60 + (v % 1000) / 10
    return np.where(v > 0, sec, np.nan)


def parse_se(b: Batch, order: np.ndarray) -> pl.DataFrame:
    n = lambda name, scale=1.0, dt=pl.Int16: _ser(name, b.num(name, 0, scale), dt)  # noqa: E731
    hw = b.num("馬体重")
    hw = np.where((hw >= 2) & (hw <= 998), hw, np.nan)
    diff = b.num("増減差")
    sign = b.str("増減符号")
    diff = np.where(diff >= 999, np.nan, np.where(sign == "-", -diff, diff))
    cols = {
        "race_key": _ser("race_key", race_key(b)),
        "umaban": n("馬番"),
        "wakuban": n("枠番"),
        "horse_id": _ser("horse_id", b.str("血統登録番号")),
        "horse_name": _ser("horse_name", b.text("馬名")),
        "sex_code": _ser("sex_code", b.str("性別コード")),
        "age": n("馬齢"),
        "belong_code": _ser("belong_code", b.str("東西所属コード")),
        "trainer_code": _ser("trainer_code", b.str("調教師コード")),
        "owner_code": _ser("owner_code", b.str("馬主コード")),
        "weight_carried": n("負担重量", 0.1, pl.Float64),
        "blinker": n("ブリンカー使用区分", dt=pl.Int8),
        "jockey_code": _ser("jockey_code", b.str("騎手コード")),
        "jockey_name": _ser("jockey_name", b.text("騎手名略称")),
        "apprentice_code": _ser("apprentice_code", b.str("騎手見習コード")),
        "horse_weight": _ser("horse_weight", hw, pl.Int16),
        "weight_diff": _ser("weight_diff", diff, pl.Int16),
        "abnormal_code": n("異常区分コード", dt=pl.Int8),
        "arrival_order": n("入線順位"),
        "finish_pos": n("確定着順"),
        "dead_heat": n("同着区分", dt=pl.Int8),
        "time_sec": _ser("time_sec", _race_time(b, "走破タイム"), pl.Float64),
        "margin_code": _ser("margin_code", b.str("着差コード")),
        "corner1": n("1コーナーでの順位"),
        "corner2": n("2コーナーでの順位"),
        "corner3": n("3コーナーでの順位"),
        "corner4": n("4コーナーでの順位"),
        "win_odds": n("単勝オッズ", 0.1, pl.Float64),
        "win_pop": n("単勝人気順"),
        "prize": _ser("prize", b.num("獲得本賞金", 0, 100.0), pl.Int64),
        "last_3f": n("後3ハロンタイム", 0.1, pl.Float64),
        "last_4f": n("後4ハロンタイム", 0.1, pl.Float64),
        "time_diff": _ser("time_diff", b.num("タイム差", 0, 0.1, signed=True), pl.Float64),
        "running_style": n("今回レース脚質判定", dt=pl.Int8),
    }
    df = pl.DataFrame({**cols, **header(b, "SE", order)})
    df = df.with_columns([_empty_to_null(df[c]) for c in df.columns if df[c].dtype == pl.String])
    zero_null = ["umaban", "wakuban", "arrival_order", "finish_pos", "win_odds", "win_pop", "age",
                 "corner1", "corner2", "corner3", "corner4"]
    def null_if(c: str, cond: pl.Expr) -> pl.Expr:
        return pl.when(cond).then(None).otherwise(pl.col(c)).alias(c)

    return df.with_columns(
        [null_if(c, pl.col(c) == 0) for c in zero_null]
        # 後3F・後4F の 999（99.9 秒）は取消・除外・中止など。タイム差の ±999 も同じ
        + [null_if(c, (pl.col(c) == 0) | (pl.col(c) >= 99.9)) for c in ("last_3f", "last_4f")]
        + [null_if("time_diff", pl.col("time_diff").abs() >= 99.9)]
    )


# ---------------------------------------------------------------- HR 払戻

BET_TYPES = [  # (仕様書のグループ名, 組番の項目名, bet_type, 不成立などのフラグの券種名)
    ("単勝払戻", "馬番", "win", "単勝"),
    ("複勝払戻", "馬番", "place", "複勝"),
    ("枠連払戻", "組番", "bracket_quinella", "枠連"),
    ("馬連払戻", "組番", "quinella", "馬連"),
    ("ワイド払戻", "組番", "wide", "ワイド"),
    ("馬単払戻", "組番", "exacta", "馬単"),
    ("3連複払戻", "組番", "trio", "3連複"),
    ("3連単払戻", "組番", "trifecta", "3連単"),
]


def parse_hr(b: Batch, order: np.ndarray) -> pl.DataFrame:
    """払戻を長い形式に。行は (race_key, bet_type, 組番) ごと。"""
    key = race_key(b)
    hdr = pl.DataFrame(header(b, "HR", order)).with_columns(race_key=pl.Series(key))
    frames = []
    for group, combo_name, bet, flag in BET_TYPES:
        f = b.layout[f"{group}.{combo_name}"]
        combo = b.str(f, None)  # (n, k)
        pay = b.num(f"{group}.払戻金", None)
        pop = b.num(f"{group}.人気順", None)
        k = combo.shape[1]
        rows = np.repeat(np.arange(len(b)), k)
        keep = (np.char.str_len(combo).ravel() > 0) & (np.char.strip(combo.ravel(), "0") != "")
        fl = {
            "not_established": b.num(f"不成立フラグ{flag}"),
            "special_payout": b.num(f"特払フラグ{flag}"),
            "refund": b.num(f"返還フラグ{flag}"),
        }
        frames.append(
            pl.DataFrame({
                "_row": rows[keep],
                "bet_type": [bet] * int(keep.sum()),
                "combination": combo.ravel()[keep],
                "payout": _ser("payout", pay.ravel()[keep], pl.Int64),
                "popularity": _ser("popularity", pop.ravel()[keep], pl.Int16),
                **{c: _ser(c, v[rows[keep]], pl.Int8) for c, v in fl.items()},
            })
        )
    long = pl.concat(frames)
    return long.join(hdr.with_row_index("_row").with_columns(pl.col("_row").cast(pl.Int64)),
                     on="_row", how="left").drop("_row")


# ---------------------------------------------------------------- O1 オッズ（単複枠）


def _odds(b: Batch, name: str) -> tuple[np.ndarray, np.ndarray]:
    raw = b.raw(name, None)  # (n, 28)
    v = b.num(name, None, 0.1)
    status = np.full(raw.shape, "ok", dtype=object)
    for code, s in _STATUS_CODE.items():
        status[raw == code] = s
    v = np.where(status == "ok", v, np.nan)
    return v, status


def parse_o1(b: Batch, order: np.ndarray, race_year: np.ndarray | None = None) -> pl.DataFrame:
    """単勝・複勝オッズを (レコード, 馬番) の長い形式に。登録のない枠（馬番が空白）は落とす。"""
    n = len(b)
    key = race_key(b)
    win_umaban = b.num("単勝オッズ.馬番", None)
    place_umaban = b.num("複勝オッズ.馬番", None)
    win, win_st = _odds(b, "単勝オッズ.オッズ")
    pmin, pmin_st = _odds(b, "複勝オッズ.最低オッズ")
    pmax, _ = _odds(b, "複勝オッズ.最高オッズ")
    wpop = b.num("単勝オッズ.人気順", None)
    ppop = b.num("複勝オッズ.人気順", None)
    wpop = np.where(win_st == "ok", wpop, np.nan)
    ppop = np.where(pmin_st == "ok", ppop, np.nan)
    k = win_umaban.shape[1]
    keep = ~np.isnan(win_umaban).ravel() & (win_umaban.ravel() > 0)
    rows = np.repeat(np.arange(n), k)[keep]
    per_rec = {
        "race_key": key,
        "announced_mdhm": b.str("発表月日時分"),
        "n_registered": b.num("登録頭数"),
        "n_starters": b.num("出走頭数"),
        "win_sale_flag": b.num("発売フラグ単勝"),
        "place_sale_flag": b.num("発売フラグ複勝"),
        "place_pay_key": b.num("複勝着払キー"),
        "win_vote_total": b.num("単勝票数合計", 0, 100.0),
        "place_vote_total": b.num("複勝票数合計", 0, 100.0),
    }
    hdr = header(b, "O1", order)
    ints = {"n_registered": pl.Int16, "n_starters": pl.Int16, "win_sale_flag": pl.Int8,
            "place_sale_flag": pl.Int8, "place_pay_key": pl.Int8,
            "win_vote_total": pl.Int64, "place_vote_total": pl.Int64}
    data = {c: _ser(c, v[rows], ints.get(c)) for c, v in per_rec.items()}
    data |= {c: s.gather(pl.Series(rows)) for c, s in hdr.items()}
    data |= {
        "umaban": _ser("umaban", win_umaban.ravel()[keep], pl.Int16),
        "win_odds": _ser("win_odds", win.ravel()[keep], pl.Float64),
        "win_pop": _ser("win_pop", wpop.ravel()[keep], pl.Int16),
        "win_status": pl.Series("win_status", win_st.ravel()[keep].tolist(), dtype=ODDS_STATUS),
        "place_odds_min": _ser("place_odds_min", pmin.ravel()[keep], pl.Float64),
        "place_odds_max": _ser("place_odds_max", pmax.ravel()[keep], pl.Float64),
        "place_pop": _ser("place_pop", ppop.ravel()[keep], pl.Int16),
        "place_status": pl.Series("place_status", pmin_st.ravel()[keep].tolist(), dtype=ODDS_STATUS),
        "_place_umaban_mismatch": pl.Series(
            "_place_umaban_mismatch", (place_umaban.ravel()[keep] != win_umaban.ravel()[keep])
        ),
    }
    return pl.DataFrame(data)


def announced_at(df: pl.DataFrame) -> pl.DataFrame:
    """発表月日時分（mmddhhmm）に年を補って announced_at を作る。

    年はレースの年。ただし月がレースの月より 6 か月以上あとなら前年（1 月のレースを 12 月に発売）、
    6 か月以上前なら翌年（12 月末のレースの確定を 1 月に発表）とする。
    """
    ry = pl.col("race_key").str.slice(0, 4).cast(pl.Int32)
    rm = pl.col("race_key").str.slice(4, 2).cast(pl.Int32)
    am = pl.col("announced_mdhm").str.slice(0, 2).cast(pl.Int32, strict=False)
    year = ry - (am - rm > 6).cast(pl.Int32) + (rm - am > 6).cast(pl.Int32)
    s = year.cast(pl.String) + pl.col("announced_mdhm")
    return df.with_columns(
        announced_at=s.str.strptime(pl.Datetime("us"), "%Y%m%d%H%M", strict=False)
    ).drop("announced_mdhm")


# ---------------------------------------------------------------- O2〜O6 オッズ（馬連・ワイド・馬単・3連複・3連単）

# レコード種別 → (bet_type, 仕様書の券種名, 組番の馬の数)。bet_type は payouts と同じ名前
EXOTIC = {
    "O2": ("quinella", "馬連", 2),
    "O3": ("wide", "ワイド", 2),
    "O4": ("exacta", "馬単", 2),
    "O5": ("trio", "3連複", 3),
    "O6": ("trifecta", "3連単", 3),
}
_STATUS_NAMES = ["ok", "no_vote", "cancel_pre", "cancel_post"]


def _status_codes(b: Batch, name: str) -> np.ndarray:
    """オッズの特殊値を (n, k) の整数（_STATUS_NAMES の位置）にする。

    桁数は券種で違う（馬連 6 桁、ワイド 5 桁、3連単 7 桁）ので、全桁が `0` / `-` / `*` かで判定する。
    """
    a = b._cols(b.layout[name], None)  # (n, k, 桁数)
    code = np.zeros(a.shape[:2], dtype=np.uint8)
    for i, ch in enumerate(b"0-*", start=1):
        code[(a == ch).all(axis=-1)] = i
    return code


def _status_series(name: str, code: np.ndarray) -> pl.Series:
    return pl.Series(name, code, dtype=pl.UInt8).replace_strict(
        dict(enumerate(_STATUS_NAMES)), return_dtype=ODDS_STATUS)


def parse_exotic(b: Batch, rtype: str, order: np.ndarray) -> pl.DataFrame:
    """O2〜O6 を (レコード, 組番) の長い形式に。組番が空白（登録なし）の枠は落とす。

    a・b・c は組番の馬番（馬単・3連単は着順の順、馬連・ワイド・3連複は小さい順）。
    ok 以外の組番はオッズと人気順を null にする。ワイドの特殊値は最低オッズで判定する。
    """
    bet, name, m = EXOTIC[rtype]
    g = f"{name}オッズ"
    combo_f = b.layout[f"{g}.組番"]
    cnum = b.num(combo_f, None)  # (n, k)。空白は NaN
    keep2 = ~np.isnan(cnum) & (cnum > 0)
    k = cnum.shape[1]
    rec = np.repeat(np.arange(len(b)), k).reshape(-1, k)[keep2]
    cv = cnum[keep2].astype(np.int64)
    um = [(cv // 100 ** (m - 1 - j)) % 100 for j in range(m)]
    combo = b.raw(combo_f, None)[keep2]
    odds_names = ["最低オッズ", "最高オッズ"] if rtype == "O3" else ["オッズ"]
    code = _status_codes(b, f"{g}.{odds_names[0]}")[keep2]
    ok = code == 0
    pop = b.num(f"{g}.人気順", None)[keep2]
    data: dict[str, pl.Series] = {"race_key": _ser("race_key", race_key(b)[rec])}
    data |= {c: _ser(c, u, pl.Int8) for c, u in zip("abc", um)}
    data["combination"] = pl.Series("combination", combo).cast(pl.String)
    cols = ["odds_min", "odds_max"] if rtype == "O3" else ["odds"]
    for col, on in zip(cols, odds_names):
        v = b.num(f"{g}.{on}", None)[keep2] / 10  # × 0.1 より誤差が小さい（1234567 → 123456.7）
        data[col] = _ser(col, np.where(ok, v, np.nan), pl.Float64)
    data["pop"] = _ser("pop", np.where(ok, pop, np.nan), pl.Int16)
    data["status"] = _status_series("status", code)
    data["vote_total"] = _ser("vote_total", b.num(f"{name}票数合計", 0, 100.0)[rec], pl.Int64)
    data["sale_flag"] = _ser("sale_flag", b.num(f"発売フラグ{name}")[rec], pl.Int8)
    hdr = header(b, rtype, order)
    idx = pl.Series(rec)
    data |= {c: s.gather(idx) for c, s in hdr.items()}
    return pl.DataFrame(data)


# ---------------------------------------------------------------- マスタ


def parse_um(b: Batch, order: np.ndarray) -> pl.DataFrame:
    ped = b.layout["3代血統情報.繁殖登録番号"]
    pedn = b.layout["3代血統情報.馬名"]
    df = pl.DataFrame({
        "horse_id": b.str("血統登録番号"),
        "horse_name": b.text("馬名"),
        "horse_name_en": b.text("馬名欧字"),
        "retired": _ser("retired", b.num("競走馬抹消区分"), pl.Int8),
        "registered_date": _date(b, "競走馬登録年月日"),
        "retired_date": _date(b, "競走馬抹消年月日"),
        "birth_date": _date(b, "生年月日"),
        "sex_code": b.str("性別コード"),
        "breed_code": b.str("品種コード"),
        "coat_code": b.str("毛色コード"),
        # 3代血統の並びは 父・母・父父・父母・母父・母母・…（仕様書の説明欄）
        "sire_id": b.str(ped, 0), "sire_name": b.text(pedn, 0),
        "dam_id": b.str(ped, 1), "dam_name": b.text(pedn, 1),
        "damsire_id": b.str(ped, 4), "damsire_name": b.text(pedn, 4),
        "belong_code": b.str("東西所属コード"),
        "trainer_code": b.str("調教師コード"),
        "breeder_code": b.str("生産者コード"),
        "birthplace": b.text("産地名"),
        "owner_code": b.str("馬主コード"),
        **header(b, "UM", order),
    })
    return df.with_columns([_empty_to_null(df[c]) for c in df.columns if df[c].dtype == pl.String])


def _person(b: Batch, order: np.ndarray, prefix: str, code_col: str, extra: dict) -> pl.DataFrame:
    df = pl.DataFrame({
        code_col: b.str(f"{prefix}コード"),
        "name": b.text(f"{prefix}名"),
        "name_kana": b.text(f"{prefix}名半角ｶﾅ"),
        "name_short": b.text(f"{prefix}名略称"),
        "name_en": b.text(f"{prefix}名欧字"),
        "retired": _ser("retired", b.num(f"{prefix}抹消区分"), pl.Int8),
        "license_date": _date(b, f"{prefix}免許交付年月日"),
        "retired_date": _date(b, f"{prefix}免許抹消年月日"),
        "birth_date": _date(b, "生年月日"),
        "sex": _ser("sex", b.num("性別区分"), pl.Int8),
        **extra,
        **header(b, prefix, order),
    })
    return df.with_columns([_empty_to_null(df[c]) for c in df.columns if df[c].dtype == pl.String])


def parse_ks(b: Batch, order: np.ndarray) -> pl.DataFrame:
    return _person(b, order, "騎手", "jockey_code", {
        "belong_code": b.str("騎手東西所属コード"),
        "apprentice_code": b.str("騎手見習コード"),
        "trainer_code": b.str("所属調教師コード"),
        "invited_region": b.text("招待地域名"),
    })


def parse_ch(b: Batch, order: np.ndarray) -> pl.DataFrame:
    return _person(b, order, "調教師", "trainer_code", {
        "belong_code": b.str("調教師東西所属コード"),
        "invited_region": b.text("招待地域名"),
    })


# ---------------------------------------------------------------- 調教


def _training(b: Batch, order: np.ndarray, fields: dict[str, str], extra: dict) -> pl.DataFrame:
    cols = {
        "center": _ser("center", b.num("トレセン区分"), pl.Int8),
        "train_date": _date(b, "調教年月日"),
        "train_time": b.str("調教時刻"),
        "horse_id": b.str("血統登録番号"),
        **extra,
    }
    for col, name in fields.items():
        v = b.num(name, 0, 0.1)
        # 0 は測定不良。9999 / 999 は上限超え（WC のみ）で、欠損として扱う
        top = 999.9 if col.startswith("total") else 99.9
        cols[col] = _ser(col, np.where((v > 0) & (v < top), v, np.nan), pl.Float64)
    return pl.DataFrame({**cols, **header(b, "HC", order)})


def parse_hc(b: Batch, order: np.ndarray) -> pl.DataFrame:
    f = {
        "total_4f": "4ハロンタイム合計(800M～0M)", "lap_800_600": "ラップタイム(800M～600M)",
        "total_3f": "3ハロンタイム合計(600M～0M)", "lap_600_400": "ラップタイム(600M～400M)",
        "total_2f": "2ハロンタイム合計(400M～0M)", "lap_400_200": "ラップタイム(400M～200M)",
        "lap_200_0": "ラップタイム(200M～0M)",
    }
    return _training(b, order, f, {})


def parse_wc(b: Batch, order: np.ndarray) -> pl.DataFrame:
    f = {}
    for k in range(10, 1, -1):
        m = k * 200
        name = "8ロンタイム合計(1600M～0M)" if k == 8 else f"{k}ハロンタイム合計({m}M～0M)"  # 仕様書の誤字のまま
        f[f"total_{k}f"] = name
    for k in range(10, 0, -1):
        m = k * 200
        f[f"lap_{m}_{m - 200}"] = f"ラップタイム({m}M～{m - 200}M)"
    extra = {
        "course": _ser("course", b.num("コース"), pl.Int8),
        "direction": _ser("direction", b.num("馬場周り"), pl.Int8),
    }
    return _training(b, order, f, extra)
