"""生データ（/mnt/e/.../raw）から parquet のテーブルを作る。

2 段に分ける。

1. 取り込み（stage）: 生ファイル 1 つ × レコード種別 1 つごとに、全版の行を parquet にする。
   ファイルの大きさと更新時刻が前回と同じなら読み直さない（差分更新）。
2. 仕上げ（finalize）: stage の全ファイルを合わせ、キーごとに最新の版を残してテーブルにする。

時系列オッズ（0B41）は版の統合が要らないので、年ごとに直接 `odds_ts_win/year=YYYY/` に書く。
0B42（馬連）は発表が多すぎるので、発走 N 分前などの発表だけを `odds_ts_quinella_snap/year=YYYY/` に書く。
O2〜O6（確定の馬連〜3連単）は大きいので、取り込みをレースの年ごとに分け、仕上げも年ごとにする。
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
EXOTIC_TYPES = tuple(T.EXOTIC)  # O2〜O6。大きいので RACE_TYPES とは別に、レースの年ごとに分けて取り込む
EXOTIC_JOBS = 4  # O2〜O6 の取り込みは 1 プロセスで数 GB 使うので、並列数をこれ以下にする

# O2〜O6 のテーブル → (レコード種別, 年ごとに分けて書くか)
EXOTIC_TABLES = {
    "odds_final_quinella": ("O2", False), "odds_final_wide": ("O3", False),
    "odds_final_exacta": ("O4", False), "odds_final_trio": ("O5", True),
    "odds_final_trifecta": ("O6", True),
}

# テーブル → 使うレコード種別
TABLES = {
    "races": ["RA"], "entries": ["SE"], "payouts": ["HR"], "odds_final": ["O1"],
    **{name: [t] for name, (t, _) in EXOTIC_TABLES.items()},
    "odds_ts_win": [], "odds_ts_quinella_snap": [], "horses": ["UM"], "jockeys": ["KS"], "trainers": ["CH"],
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
    # O2〜O6: file_no は --years によらず決まるように、年ファイルは年、update は全 update の中の順番 + 100000
    exotic_t = tuple(t for t in EXOTIC_TYPES if t in types)
    if exotic_t:
        numbered += [Source(p, "RACE", exotic_t, int(p.stem) if p.stem.isdigit() else 0)
                     for p in sorted((raw / "RACE").glob("*.txt")) if year_ok(p)]
        numbered += [Source(p, "RACE_update", exotic_t, 100_000 + i)
                     for i, p in enumerate(sorted((raw / "RACE" / "update").glob("*.txt")))]
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


def _stage_exotic(src: Source, stage: Path, spec: Path, chunk: int = 256) -> dict:
    """O2〜O6 の取り込み。レコードの一覧（meta）と、レースの年ごとの組番の行を別々の parquet にする。

    3連単は 1 レコード 4,896 組なので、chunk レコードずつ展開してメモリを抑える。
    """
    layouts = load_layouts(spec)
    recs = read_records(src.path, src.types)
    stats = {}
    d = stage / src.group
    d.mkdir(parents=True, exist_ok=True)
    for t in src.types:
        for old in d.glob(f"{src.path.stem}__{t}__*.parquet"):
            old.unlink()
        lines = recs.pop(t)
        b = Batch(layouts[t], lines)
        del lines
        n_all, bad = len(b), b.bad_length
        b = b.take(np.nonzero(T.jra_rows(b))[0])
        order = src.file_no * 10_000_000_000 + np.arange(len(b))
        meta = pl.DataFrame({"race_key": T.race_key(b), **T.header(b, t, order)})
        meta.write_parquet(d / f"{src.path.stem}__{t}__meta.parquet")
        frames = [T.parse_exotic(b.take(np.arange(i, min(i + chunk, len(b)))), t, order[i : i + chunk])
                  for i in range(0, len(b), chunk)]
        del b
        df = pl.concat(frames) if frames else None
        del frames
        years = []
        if df is not None and df.height:
            df = df.with_columns(_y=pl.col("race_key").str.slice(0, 4))
            for (y,), part in df.partition_by("_y", as_dict=True).items():
                part.drop("_y").write_parquet(d / f"{src.path.stem}__{t}__y{y}.parquet")
                years.append(int(y))
        stats[t] = {"lines": n_all, "kept": meta.height, "rows": 0 if df is None else df.height,
                    "bad_length": bad, "years": sorted(years)}
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
    # O2〜O6 は 1 プロセスで数 GB 使うので並列数を抑える
    exotic = [(k, s) for k, s in todo if set(s.types) <= set(EXOTIC_TYPES)]
    other = [(k, s) for k, s in todo if (k, s) not in exotic]
    for batch, fn, n in [(other, _stage_one, jobs), (exotic, _stage_exotic, min(jobs, EXOTIC_JOBS))]:
        if batch:
            _stage_run(paths, state, state_path, batch, fn, n)


def _stage_run(paths: Paths, state: dict, state_path: Path, todo: list, fn, jobs: int) -> None:
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(fn, s, paths.stage, paths.spec): (key, s) for key, s in todo}
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


# ---------------------------------------------------------------- 確定オッズ O2〜O6


def _exotic_cols(rtype: str) -> list[str]:
    um = ["a", "b", "c"][: T.EXOTIC[rtype][2]]
    odds = ["odds_min", "odds_max"] if rtype == "O3" else ["odds"]
    return ["race_key", *um, "combination", *odds, "pop", "status", "vote_total", "sale_flag",
            "data_kubun", "created_date"]


def build_exotic(paths: Paths, races: pl.DataFrame, name: str) -> int:
    """O2〜O6 の確定オッズ。レースごとに最新のレコードを選び、そのレコードの組番を全部残す。

    取り込みはレースの年ごとに分けてあるので、仕上げも年ごとに読む。partitioned なら
    `<name>/year=YYYY/part-000.parquet`、そうでなければ 1 ファイルにまとめる。
    """
    rtype, partitioned = EXOTIC_TABLES[name]
    metas = sorted(paths.stage.glob(f"*/*__{rtype}__meta.parquet"))
    if not metas:
        raise FileNotFoundError(f"{rtype} の stage がない。先に取り込む")
    meta = pl.concat([pl.read_parquet(f) for f in metas], how="vertical_relaxed")
    best = T.latest(meta.with_columns(_o=pl.col("_order")), ["race_key"])
    best = best.filter(pl.col("data_kubun") != "0").join(races.select("race_key"), on="race_key", how="semi")
    best = best.select(pl.col("_o").alias("_order"))
    years = sorted({f.stem.rsplit("__y", 1)[1] for f in paths.stage.glob(f"*/*__{rtype}__y*.parquet")})
    cols, keys = _exotic_cols(rtype), [c for c in ("race_key", "a", "b", "c") if c in _exotic_cols(rtype)]
    tmp = paths.out / f".tmp_{name}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    total, frames = 0, []
    for y in years:
        files = sorted(paths.stage.glob(f"*/*__{rtype}__y{y}.parquet"))
        df = pl.concat([pl.read_parquet(f).join(best, on="_order", how="semi") for f in files],
                       how="vertical_relaxed").select(cols).sort(keys)
        total += df.height
        if partitioned:
            (tmp / f"year={y}").mkdir()
            df.write_parquet(tmp / f"year={y}" / "part-000.parquet")
        else:
            frames.append(df)
        log.info("  %s %s: %d 行", name, y, df.height)
    if partitioned:
        dest = paths.out / name
        shutil.rmtree(dest, ignore_errors=True)
        tmp.rename(dest)
    else:
        pl.concat(frames).write_parquet(paths.out / f"{name}.parquet")
        shutil.rmtree(tmp)
    return total


# ---------------------------------------------------------------- 時系列オッズ（0B41）


def _ts_chunk(files: list[str], out_file: str, spec: str) -> dict:
    layout = load_layouts(Path(spec))["O1"]
    lines, stats = _read_ts_files(files, "O1")
    b = Batch(layout, lines)
    stats |= {"records": len(b), "bad_length": b.bad_length}
    if not len(b):
        return stats
    # 同じ発表時刻（分単位）に 2 回発表されることがある
    keep = _dedup_same_minute(b, "単勝票数合計")
    stats["duplicate_records"] = len(b) - len(keep)
    b = b.take(keep)
    df = T.announced_at(T.parse_o1(b, np.arange(len(b))))
    stats["mdhm_unparsed"] = int(df["announced_at"].null_count())
    stats["place_umaban_mismatch"] = int(df["_place_umaban_mismatch"].sum())
    cols = ["race_key", "announced_at", "data_kubun", "umaban", "win_odds", "win_pop", "win_status",
            "place_odds_min", "place_odds_max", "place_pop", "place_status", "n_starters",
            "win_sale_flag", "place_sale_flag", "win_vote_total", "place_vote_total", "created_date"]
    df.select(cols).sort(["race_key", "announced_at", "data_kubun", "umaban"]).write_parquet(out_file)
    stats["rows"] = df.height
    return stats


def _ts_years(paths: Paths, src_dir: str, out_name: str, state_name: str, years: set[int] | None, jobs: int,
              force: bool, chunk: int, submit) -> None:
    """時系列オッズの年フォルダごとの組み立て。フォルダのファイル数・大きさ・更新時刻が変わった年だけ作り直す。

    submit(ex, y, files, out_file) が 1 チャンク分の Future を返す。
    """
    src = paths.raw / src_dir
    out = paths.out / out_name
    state_path = paths.stage / state_name
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
            futs = [submit(ex, y, p, str(tmp / f"part-{i:03d}.parquet")) for i, p in enumerate(parts)]
            for fut in as_completed(futs):
                for k, v in fut.result().items():
                    total[k] = total.get(k, 0) + v
        shutil.rmtree(odir, ignore_errors=True)
        tmp.rename(odir)
        state[str(y)] = {"sig": sig, "stats": total}
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1))
        log.info("%s %d: %s", out_name, y, total)


def build_odds_ts(paths: Paths, years: set[int] | None, jobs: int, force: bool, chunk: int = 400) -> None:
    _ts_years(paths, "0B41", "odds_ts_win", "_state_odds_ts.json", years, jobs, force, chunk,
              lambda ex, y, files, out_file: ex.submit(_ts_chunk, files, out_file, str(paths.spec)))


# ---------------------------------------------------------------- 時系列オッズ 馬連（0B42）の発走前スナップショット

SNAP_MINUTES = (1, 2, 5, 10, 30, 60)
SNAP_LABELS = [*(str(n) for n in SNAP_MINUTES), "last"]


def _read_ts_files(files: list[str], rtype: str) -> tuple[list[bytes], dict]:
    lines, mismatch, empty = [], 0, 0
    for f in files:
        recs = read_records(Path(f), [rtype])[rtype]
        if not recs:
            empty += 1
        stem = Path(f).stem.encode()
        mismatch += sum(r[11:27] != stem for r in recs)
        lines += recs
    return lines, {"files": len(files), "empty_files": empty, "key_mismatch": mismatch}


def _dedup_same_minute(b: Batch, vote_field: str) -> np.ndarray:
    """同じ race_key・データ区分・発表月日時分の発表が 2 つ以上あれば、票数合計が多い方（後の発表）を残す。
    同じならファイルで後の行。残す行の位置を昇順で返す。"""
    rec = pl.DataFrame({
        "k": T.race_key(b), "kb": b.str("データ区分"), "t": b.str("発表月日時分"),
        "v": np.nan_to_num(b.num(vote_field), nan=-1.0),
    }).with_row_index("i")
    rec = rec.sort(["k", "kb", "t", "v", "i"])
    return np.sort(rec.unique(subset=["k", "kb", "t"], keep="last", maintain_order=True)["i"].to_numpy())


def select_snapshots(rec: pl.DataFrame, minutes=SNAP_MINUTES) -> pl.DataFrame:
    """発表の一覧（i, race_key, data_kubun, announced_at, post_at）から、スナップショットに使う発表を選ぶ。

    N 分前: データ区分 1（中間）で announced_at <= post_at - N 分の最後の発表。
    last: 全発表の最後（announced_at → データ区分の順位 → 読んだ順）。
    戻り値は (i, snap, announced_at)。1 つの発表が複数の snap に使われれば、その数だけ行がある。
    """
    rank = T.KUBUN_RANK["O2"]
    mid = rec.filter((pl.col("data_kubun") == "1") & pl.col("announced_at").is_not_null()
                     & pl.col("post_at").is_not_null())
    out = []
    for n in minutes:
        c = mid.filter(pl.col("announced_at") <= pl.col("post_at") - pl.duration(minutes=n))
        c = c.sort(["race_key", "announced_at", "i"]).unique("race_key", keep="last", maintain_order=True)
        out.append(c.select("i", pl.lit(str(n)).alias("snap"), "announced_at"))
    last = (rec.with_columns(_r=pl.col("data_kubun").replace_strict(rank, default=0, return_dtype=pl.Int8))
            .sort(["race_key", "announced_at", "_r", "i"], nulls_last=False)
            .unique("race_key", keep="last", maintain_order=True))
    out.append(last.select("i", pl.lit("last").alias("snap"), "announced_at"))
    return pl.concat(out)


def _snap_chunk(files: list[str], out_file: str, spec: str, post: pl.DataFrame) -> dict:
    layout = load_layouts(Path(spec))["O2"]
    lines, stats = _read_ts_files(files, "O2")
    b = Batch(layout, lines)
    del lines
    stats |= {"records": len(b), "bad_length": b.bad_length}
    if not len(b):
        return stats
    keep = _dedup_same_minute(b, "馬連票数合計")
    stats["duplicate_records"] = len(b) - len(keep)
    b = b.take(keep)
    rec = T.announced_at(pl.DataFrame({
        "race_key": T.race_key(b), "data_kubun": b.str("データ区分"), "announced_mdhm": b.str("発表月日時分"),
    }).with_row_index("i").with_columns(pl.col("i").cast(pl.Int64)))
    stats["mdhm_unparsed"] = int(rec.filter(pl.col("data_kubun") == "1")["announced_at"].null_count())
    rec = rec.join(post, on="race_key", how="left")
    stats["races"] = rec["race_key"].n_unique()
    stats["races_without_post_at"] = rec.filter(pl.col("post_at").is_null())["race_key"].n_unique()
    sel = select_snapshots(rec)
    df = T.parse_exotic(b.take(sel["i"].to_numpy()), "O2", np.arange(sel.height))
    sel = sel.with_row_index("_order").with_columns(pl.col("_order").cast(pl.Int64))
    df = df.join(sel.select("_order", "snap", "announced_at"), on="_order", how="left")
    snap_no = pl.col("snap").replace_strict({s: i for i, s in enumerate(SNAP_LABELS)}, return_dtype=pl.Int8)
    cols = ["race_key", "snap", "announced_at", "data_kubun", "a", "b", "combination", "odds", "pop", "status",
            "vote_total", "created_date"]
    df.sort(["race_key", snap_no, "a", "b"]).select(cols).write_parquet(out_file)
    for s in SNAP_LABELS:
        stats[f"races_snap_{s}"] = int((sel["snap"] == s).sum())
    stats["rows"] = df.height
    return stats


def build_odds_ts_quinella_snap(paths: Paths, years: set[int] | None, jobs: int, force: bool,
                                chunk: int = 300) -> None:
    races = pl.read_parquet(paths.out / "races.parquet", columns=["race_key", "post_at"])

    def submit(ex, y, files, out_file):
        keys = [Path(f).stem for f in files]
        post = races.filter(pl.col("race_key").is_in(keys))
        return ex.submit(_snap_chunk, files, out_file, str(paths.spec), post)

    _ts_years(paths, "0B42", "odds_ts_quinella_snap", "_state_odds_ts_quinella_snap.json", years, jobs, force,
              chunk, submit)


# ---------------------------------------------------------------- 全体


def run(paths: Paths, tables: list[str], years: set[int] | None, jobs: int, force: bool) -> None:
    types = {t for name in tables for t in TABLES[name]}
    if types - {"UM", "KS", "CH", "HC", "WC"}:
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
    for name in EXOTIC_TABLES:
        if name in tables:
            info[name] = {"rows": build_exotic(paths, races, name)}
            log.info("%s: %d 行", name, info[name]["rows"])
    if "odds_ts_win" in tables:
        build_odds_ts(paths, years, jobs, force)
    if "odds_ts_quinella_snap" in tables:  # races.parquet の発走時刻を使う
        build_odds_ts_quinella_snap(paths, years, jobs, force)
    info_path.write_text(json.dumps(info, ensure_ascii=False, indent=1))
