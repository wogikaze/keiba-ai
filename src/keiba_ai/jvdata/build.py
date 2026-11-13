"""生データ（/mnt/e/.../raw）から parquet のテーブルを作る。

2 段に分ける。

1. 取り込み（stage）: 生ファイル 1 つ × レコード種別 1 つごとに、全版の行を parquet にする。
   ファイルの大きさと更新時刻が前回と同じなら読み直さない（差分更新）。
2. 仕上げ（finalize）: stage の全ファイルを合わせ、キーごとに最新の版を残してテーブルにする。

時系列オッズ（0B41）は版の統合が要らないので、年ごとに直接 `odds_ts_win/year=YYYY/` に書く。
"""

from __future__ import annotations

import json
import logging
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import polars as pl

from . import tables as T
from .layout import DEFAULT_SPEC, load_layouts
from .parse import Batch, read_records

log = logging.getLogger(__name__)

# 取り込みの処理を変えたら上げる。上げると stage を作り直す。
STAGE_VERSION = 1

PARSERS = {
    "RA": T.parse_ra, "SE": T.parse_se, "HR": T.parse_hr, "O1": T.parse_o1,
    "UM": T.parse_um, "KS": T.parse_ks, "CH": T.parse_ch, "HC": T.parse_hc, "WC": T.parse_wc,
}
RACE_TYPES = ("RA", "SE", "HR", "O1")

# テーブル → 使うレコード種別
TABLES = {
    "races": ["RA"], "entries": ["SE"], "payouts": ["HR"], "odds_final": ["O1"],
    "odds_ts_win": [], "horses": ["UM"], "jockeys": ["KS"], "trainers": ["CH"],
    "training_slope": ["HC"], "training_wood": ["WC"],
}


@dataclass
class Paths:
    raw: Path
    out: Path
    spec: Path = DEFAULT_SPEC

    @property
    def stage(self) -> Path:
        return self.out / "_stage"


# ---------------------------------------------------------------- 取り込み


@dataclass(frozen=True)
class Source:
    """生ファイル 1 つ。file_no は版の同点を崩す順番（後から提供されたものほど大きく）。"""

    path: Path
    group: str  # RACE / RACE_update / DIFN / SLOP / WOOD
    types: tuple[str, ...]
    file_no: int

    @property
    def stage_name(self) -> str:
        return f"{self.group}/{self.path.stem}"


def list_sources(raw: Path, types: set[str], years: set[int] | None) -> list[Source]:
    def year_ok(p: Path) -> bool:
        return years is None or not p.stem.isdigit() or int(p.stem) in years

    out: list[Source] = []
    race_t = tuple(t for t in RACE_TYPES if t in types)
    if race_t:
        files = sorted(p for p in (raw / "RACE").glob("*.txt") if year_ok(p))
        out += [Source(p, "RACE", race_t, 0) for p in files]
        # update/ は毎日の差分。年ファイルの年によらず全部読む
        out += [Source(p, "RACE_update", race_t, 0) for p in sorted((raw / "RACE" / "update").glob("*.txt"))]
    master_t = tuple(t for t in ("UM", "KS", "CH") if t in types)
    if master_t and (raw / "DIFN" / "all.txt").exists():
        out.append(Source(raw / "DIFN" / "all.txt", "DIFN", master_t, 0))
    if "HC" in types:
        out += [Source(p, "SLOP", ("HC",), 0) for p in sorted((raw / "SLOP").glob("*.txt")) if year_ok(p)]
    if "WC" in types and (raw / "WOOD" / "all.txt").exists():
        out.append(Source(raw / "WOOD" / "all.txt", "WOOD", ("WC",), 0))
    # file_no: グループ内の名前順（年 → update の日付順）
    numbered = []
    for i, s in enumerate(out):
        numbered.append(Source(s.path, s.group, s.types, i + (1000 if s.group == "RACE_update" else 0)))
    return numbered


def _sig(p: Path) -> dict:
    st = p.stat()
    return {"size": st.st_size, "mtime_ns": st.st_mtime_ns, "version": STAGE_VERSION}


def _stage_one(src: Source, stage: Path, spec: Path) -> dict:
    layouts = load_layouts(spec)
    recs = read_records(src.path, src.types)
    stats = {}
    d = stage / src.group
    d.mkdir(parents=True, exist_ok=True)
    for t in src.types:
        b = Batch(layouts[t], recs.pop(t))
        n_all = len(b)
        if t in RACE_TYPES:
            b = b.take(np.nonzero(T.jra_rows(b))[0])
        order = src.file_no * 10_000_000_000 + np.arange(len(b))
        df = PARSERS[t](b, order)
        df.write_parquet(d / f"{src.path.stem}__{t}.parquet")
        stats[t] = {"lines": n_all, "kept": len(b), "rows": df.height, "bad_length": b.bad_length}
    return {"source": str(src.path), "stats": stats}


def _load_state(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def stage(paths: Paths, types: set[str], years: set[int] | None, jobs: int, force: bool) -> None:
    state_path = paths.stage / "_state.json"
    state = _load_state(state_path)
    todo = []
    for s in list_sources(paths.raw, types, years):
        key = f"{s.stage_name}:{','.join(s.types)}"
        if not force and state.get(key, {}).get("sig") == _sig(s.path):
            continue
        todo.append((key, s))
    log.info("取り込み: %d ファイル（変更なしで飛ばしたものを除く）", len(todo))
    if not todo:
        return
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(_stage_one, s, paths.stage, paths.spec): (key, s) for key, s in todo}
        for fut in as_completed(futs):
            key, s = futs[fut]
            res = fut.result()
            state[key] = {"sig": _sig(s.path), "stats": res["stats"]}
            log.info("  %s %s", s.stage_name, {t: v["rows"] for t, v in res["stats"].items()})
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1))


def _scan_stage(stage_dir: Path, rtype: str) -> pl.DataFrame:
    files = sorted(stage_dir.glob(f"*/*__{rtype}.parquet"))
    if not files:
        raise FileNotFoundError(f"{rtype} の stage がない。先に取り込む")
    return pl.concat([pl.read_parquet(f) for f in files], how="vertical_relaxed")


# ---------------------------------------------------------------- 仕上げ


def _latest_records(df: pl.DataFrame, keys: list[str]) -> pl.DataFrame:
    """長い形式（1 レコードが複数行）の表で、キーごとに最新のレコードの行だけを残す。"""
    recs = df.select([*keys, "created_date", "_rank", "_order", "data_kubun"]).unique()
    best = T.latest(recs.with_columns(_o=pl.col("_order")), keys).select(pl.col("_o").alias("_order"))
    return df.join(best, on="_order", how="semi").drop(["_rank", "_order"])


RACE_COLS = [
    "race_key", "date", "year", "venue_code", "kai", "nichi", "race_no", "weekday_code", "post_time", "post_at",
    "race_name", "race_subname", "race_name_paren", "race_name_short", "special_race_no", "grade_code",
    "race_type_code", "race_symbol_code", "weight_type_code", "cond_2yo", "cond_3yo", "cond_4yo", "cond_5up",
    "cond_youngest", "distance", "track_code", "surface", "course_kubun", "weather_code", "going_code",
    "turf_going_code", "dirt_going_code", "n_registered", "n_starters", "n_finishers", "prize_1st",
    "first_3f", "first_4f", "last_3f", "last_4f", "record_flag", "is_cancelled", "data_kubun", "created_date",
]


def build_races(paths: Paths) -> pl.DataFrame:
    df = T.latest(_scan_stage(paths.stage, "RA"), ["race_key"])
    return df.with_columns(is_cancelled=pl.col("data_kubun") == "9").select(RACE_COLS).sort("race_key")


def build_entries(paths: Paths, races: pl.DataFrame) -> tuple[pl.DataFrame, dict]:
    raw = _scan_stage(paths.stage, "SE")
    df = T.latest(raw.with_columns(_r=pl.col("_rank")), ["race_key", "horse_id"])
    # 古い版にしかいない馬（出馬表の前に回避した馬など）を落とす: レース内の最大の版より低い行
    stale = pl.col("_r") < pl.col("_r").max().over("race_key")
    info = {"stale_dropped": int(df.filter(stale).height),
            "not_in_races": int(df.join(races, on="race_key", how="anti").height)}
    df = df.filter(~stale).drop("_r").join(races.select("race_key"), on="race_key", how="semi")
    return df.sort(["race_key", "umaban"]), info


def build_payouts(paths: Paths, races: pl.DataFrame) -> pl.DataFrame:
    df = _latest_records(_scan_stage(paths.stage, "HR"), ["race_key"])
    df = df.filter(pl.col("data_kubun") != "0").join(races.select("race_key"), on="race_key", how="semi")
    cols = ["race_key", "bet_type", "combination", "payout", "popularity",
            "not_established", "special_payout", "refund", "data_kubun", "created_date"]
    return df.select(cols).sort(["race_key", "bet_type", "combination"])


ODDS_COLS = [
    "race_key", "umaban", "win_odds", "win_pop", "win_status", "place_odds_min", "place_odds_max", "place_pop",
    "place_status", "n_registered", "n_starters", "win_sale_flag", "place_sale_flag", "place_pay_key",
    "win_vote_total", "place_vote_total", "data_kubun", "created_date",
]


def build_odds_final(paths: Paths, races: pl.DataFrame) -> pl.DataFrame:
    df = _latest_records(_scan_stage(paths.stage, "O1"), ["race_key"])
    df = df.filter(pl.col("data_kubun") != "0").join(races.select("race_key"), on="race_key", how="semi")
    return df.select(ODDS_COLS).sort(["race_key", "umaban"])


def build_master(paths: Paths, rtype: str, key: str) -> pl.DataFrame:
    return T.latest(_scan_stage(paths.stage, rtype), [key]).sort(key)


def build_training(paths: Paths, rtype: str) -> pl.DataFrame:
    df = T.latest(_scan_stage(paths.stage, rtype), ["center", "train_date", "train_time", "horse_id"])
    return df.sort(["train_date", "horse_id", "train_time"])


# ---------------------------------------------------------------- 時系列オッズ（0B41）


def _ts_chunk(files: list[str], out_file: str, spec: str) -> dict:
    layout = load_layouts(Path(spec))["O1"]
    lines, mismatch, empty = [], 0, 0
    for f in files:
        recs = read_records(Path(f), ["O1"])["O1"]
        if not recs:
            empty += 1
        stem = Path(f).stem.encode()
        mismatch += sum(r[11:27] != stem for r in recs)
        lines += recs
    b = Batch(layout, lines)
    stats = {"files": len(files), "empty_files": empty, "records": len(b),
             "bad_length": b.bad_length, "key_mismatch": mismatch}
    if not len(b):
        return stats
    # 同じ発表時刻（分単位）に 2 回発表されることがある。単勝票数合計が多い方（後の発表）を残し、
    # 同じならファイルで後の行を残す
    rec = pl.DataFrame({
        "k": T.race_key(b), "kb": b.str("データ区分"), "t": b.str("発表月日時分"),
        "v": np.nan_to_num(b.num("単勝票数合計"), nan=-1.0),
    }).with_row_index("i")
    rec = rec.sort(["k", "kb", "t", "v", "i"])
    keep = rec.unique(subset=["k", "kb", "t"], keep="last", maintain_order=True)["i"].to_numpy()
    stats["duplicate_records"] = len(b) - len(keep)
    b = b.take(np.sort(keep))
    df = T.announced_at(T.parse_o1(b, np.arange(len(b))))
    stats["mdhm_unparsed"] = int(df["announced_at"].null_count())
    stats["place_umaban_mismatch"] = int(df["_place_umaban_mismatch"].sum())
    cols = ["race_key", "announced_at", "data_kubun", "umaban", "win_odds", "win_pop", "win_status",
            "place_odds_min", "place_odds_max", "place_pop", "place_status", "n_starters",
            "win_sale_flag", "place_sale_flag", "win_vote_total", "place_vote_total", "created_date"]
    df.select(cols).sort(["race_key", "announced_at", "data_kubun", "umaban"]).write_parquet(out_file)
    stats["rows"] = df.height
    return stats


def build_odds_ts(paths: Paths, years: set[int] | None, jobs: int, force: bool, chunk: int = 400) -> None:
    src = paths.raw / "0B41"
    out = paths.out / "odds_ts_win"
    state_path = paths.stage / "_state_odds_ts.json"
    state = _load_state(state_path)
    for ydir in sorted(p for p in src.iterdir() if p.is_dir() and p.name.isdigit()):
        y = int(ydir.name)
        if years is not None and y not in years:
            continue
        files = sorted(e.path for e in os.scandir(ydir) if e.name.endswith(".txt"))
        # E: ドライブ（WSL の drvfs）は stat が遅いので並列に取る
        with ThreadPoolExecutor(max_workers=32) as tp:
            stats = list(tp.map(os.stat, files))
        sig = {"n": len(files), "size": sum(st.st_size for st in stats),
               "mtime": max((st.st_mtime_ns for st in stats), default=0), "version": STAGE_VERSION}
        odir = out / f"year={y}"
        if not force and state.get(str(y), {}).get("sig") == sig and odir.exists():
            continue
        tmp = out / f".tmp_year={y}"
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        parts = [files[i : i + chunk] for i in range(0, len(files), chunk)]
        total: dict[str, int] = {}
        with ProcessPoolExecutor(max_workers=jobs) as ex:
            futs = [ex.submit(_ts_chunk, p, str(tmp / f"part-{i:03d}.parquet"), str(paths.spec))
                    for i, p in enumerate(parts)]
            for fut in as_completed(futs):
                for k, v in fut.result().items():
                    total[k] = total.get(k, 0) + v
        shutil.rmtree(odir, ignore_errors=True)
        tmp.rename(odir)
        state[str(y)] = {"sig": sig, "stats": total}
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1))
        log.info("odds_ts_win %d: %s", y, total)


# ---------------------------------------------------------------- 全体


def run(paths: Paths, tables: list[str], years: set[int] | None, jobs: int, force: bool) -> None:
    types = {t for name in tables for t in TABLES[name]}
    if "entries" in tables or "payouts" in tables or "odds_final" in tables:
        types.add("RA")  # レースの一覧で絞る
    if types:
        stage(paths, types, years, jobs, force)
    paths.out.mkdir(parents=True, exist_ok=True)
    info_path = paths.out / "_build_info.json"
    info = _load_state(info_path)

    def write(name: str, df: pl.DataFrame) -> None:
        df.write_parquet(paths.out / f"{name}.parquet")
        info[name] = {"rows": df.height}
        log.info("%s: %d 行", name, df.height)

    races = None
    if types & set(RACE_TYPES):
        races = build_races(paths)
        if "races" in tables:
            write("races", races)
    if "entries" in tables:
        df, extra = build_entries(paths, races)
        write("entries", df)
        info["entries"] |= extra
    if "payouts" in tables:
        write("payouts", build_payouts(paths, races))
    if "odds_final" in tables:
        write("odds_final", build_odds_final(paths, races))
    for name, rtype, key in [("horses", "UM", "horse_id"), ("jockeys", "KS", "jockey_code"),
                             ("trainers", "CH", "trainer_code")]:
        if name in tables:
            write(name, build_master(paths, rtype, key))
    for name, rtype in [("training_slope", "HC"), ("training_wood", "WC")]:
        if name in tables:
            write(name, build_training(paths, rtype))
    if "odds_ts_win" in tables:
        build_odds_ts(paths, years, jobs, force)
    info_path.write_text(json.dumps(info, ensure_ascii=False, indent=1))
