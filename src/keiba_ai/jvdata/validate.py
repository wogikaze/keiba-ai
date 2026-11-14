"""作ったテーブルの検証。集計値だけを Markdown で返す（個々のレースの行は出さない）。"""

from __future__ import annotations

import json

import polars as pl

from .build import Paths


def _md(df: pl.DataFrame) -> str:
    cols = df.columns
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.iter_rows():
        lines.append("| " + " | ".join("" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v)) for v in r) + " |")
    return "\n".join(lines)


def _pct(a: int, b: int) -> str:
    return f"{a:,} / {b:,}（{100 * a / b:.2f}%）" if b else f"{a} / 0"


def report(paths: Paths) -> str:
    d = paths.out
    out: list[str] = []
    ra = pl.read_parquet(d / "races.parquet")
    se = pl.read_parquet(d / "entries.parquet")
    hr = pl.read_parquet(d / "payouts.parquet")
    o1 = pl.read_parquet(d / "odds_final.parquet")
    info = json.loads((d / "_build_info.json").read_text())

    # ---- races
    out.append("## races: 年ごとのレース数\n")
    by_year = ra.group_by("year").agg(
        races=pl.len(), cancelled=pl.col("is_cancelled").sum(),
        no_post_time=pl.col("post_at").is_null().sum(),
    ).sort("year")
    old = by_year.filter(pl.col("year") < 1986)
    out.append(f"1986 年より前の開催日を持つレース: {old['races'].sum()} 件（{old['year'].min()}〜{old['year'].max()} 年）。\n")
    out.append(_md(by_year.filter(pl.col("year") >= 1986)) + "\n")

    # ---- entries
    # 1986 年より前のレースは一部の馬しか入っていないので、entries の検査から外す
    held = ra.filter(~pl.col("is_cancelled") & (pl.col("year") >= 1986))
    per_race = se.group_by("race_key").agg(n=pl.len())
    out.append("## entries\n")
    out.append(f"- 頭数（1 レースあたりの行数）: 最小 {per_race['n'].min()}、中央値 {per_race['n'].median():.0f}、"
               f"平均 {per_race['n'].mean():.2f}、最大 {per_race['n'].max()}。")
    out.append(f"- 最新版の SE のうち races にないレース: {info['entries']['not_in_races']} 行。"
               f"古い版にしか残っていない馬として落とした行: {info['entries']['stale_dropped']} 行。")
    no_se = held.join(per_race, on="race_key", how="anti")
    out.append(f"- 開催されたレースで SE が 1 行もないもの: {no_se.height} 件。")
    n_runner = se.filter(~pl.col("abnormal_code").is_in([1, 2, 3])).group_by("race_key").agg(n=pl.len())
    cmp_n = held.join(n_runner, on="race_key").filter(pl.col("n") != pl.col("n_starters"))
    out.append(f"- 出走頭数（RA）と、取消・除外を除いた SE の行数が違うレース: {cmp_n.height} 件。")
    wins = se.filter(pl.col("finish_pos") == 1).group_by("race_key").agg(n1=pl.len(), dh=pl.col("dead_heat").max())
    w = held.join(wins, on="race_key", how="left").with_columns(pl.col("n1").fill_null(0))
    wc = w.group_by("n1").agg(races=pl.len(), with_dead_heat_flag=(pl.col("dh") == 1).sum()).sort("n1")
    out.append("- 1 着の頭数ごとのレース数（1986 年以降、中止を除く）:\n")
    out.append(_md(wc) + "\n")

    # ---- SE の単勝オッズ vs O1 確定オッズ
    j = se.select("race_key", "umaban", se_odds="win_odds", se_pop="win_pop").join(
        o1.select("race_key", "umaban", "win_odds", "win_pop", "win_status"), on=["race_key", "umaban"], how="inner")
    both = j.filter(pl.col("se_odds").is_not_null() & pl.col("win_odds").is_not_null())
    eq = both.filter((pl.col("se_odds") - pl.col("win_odds")).abs() < 0.05)
    out.append("## SE の単勝オッズと O1（確定）の単勝オッズ\n")
    out.append(f"- 両方に馬番がある行: {j.height:,}。両方に値がある行: {both.height:,}。")
    out.append(f"- 一致（差 0.05 未満）: {_pct(eq.height, both.height)}。")
    pop_eq = both.filter(pl.col("se_pop") == pl.col("win_pop")).height
    out.append(f"- 人気順の一致: {_pct(pop_eq, both.height)}。")
    only_se = j.filter(pl.col("se_odds").is_not_null() & pl.col("win_odds").is_null()).height
    only_o1 = j.filter(pl.col("se_odds").is_null() & pl.col("win_odds").is_not_null()).height
    out.append(f"- SE だけ値がある: {only_se:,} 行、O1 だけ値がある: {only_o1:,} 行。")
    o1_races = o1["race_key"].n_unique()
    out.append(f"- O1 があるレース: {o1_races:,}（最初のレース {o1['race_key'].min()[:8]}）。\n")

    # ---- HR 単勝払戻 vs 単勝オッズ × 100
    win_pay = hr.filter(pl.col("bet_type") == "win").with_columns(umaban=pl.col("combination").cast(pl.Int16))
    wj = win_pay.join(o1.select("race_key", "umaban", "win_odds"), on=["race_key", "umaban"], how="inner")
    wj = wj.with_columns(exp=(pl.col("win_odds") * 100).round(0))
    dh_races = win_pay.group_by("race_key").agg(n=pl.len()).filter(pl.col("n") > 1)
    wj_single = wj.join(dh_races, on="race_key", how="anti")
    ok = wj_single.filter(pl.col("payout") == pl.col("exp")).height
    out.append("## HR の単勝払戻と O1 の単勝オッズ × 100\n")
    out.append(f"- 単勝の払戻行: {win_pay.height:,}（同着で 2 頭以上に払戻したレース {dh_races.height}）。")
    out.append(f"- 1 着が 1 頭のレースで payout = オッズ × 100: {_pct(ok, wj_single.height)}。")
    bad = wj_single.filter(pl.col("payout") != pl.col("exp")).with_columns(
        diff=(pl.col("payout") - pl.col("exp")))
    if bad.height:
        out.append(f"- 一致しない行の差（円）: 最小 {bad['diff'].min():.0f}、最大 {bad['diff'].max():.0f}、"
                   f"特払 {int((bad['special_payout'] == 1).sum())} 行。")
    se_win = se.filter(pl.col("finish_pos") == 1).select("race_key", "umaban")
    hit = win_pay.join(se_win, on=["race_key", "umaban"], how="semi").height
    out.append(f"- 単勝の払戻馬番が SE の 1 着馬と一致: {_pct(hit, win_pay.height)}。\n")

    if (d / "odds_ts_win").exists():
        out.append(ts_report(paths, ra, o1))
    if (d / "odds_final_quinella.parquet").exists():
        out.append(exotic_report(paths, hr))
    if (d / "odds_ts_quinella_snap").exists():
        out.append(snap_report(paths, ra))
    return "\n".join(out)


EXOTIC_NAMES = [("odds_final_quinella", "quinella"), ("odds_final_wide", "wide"), ("odds_final_exacta", "exacta"),
                ("odds_final_trio", "trio"), ("odds_final_trifecta", "trifecta")]


def _scan_table(d, name: str) -> pl.LazyFrame:
    if (d / f"{name}.parquet").exists():
        return pl.scan_parquet(d / f"{name}.parquet")
    return pl.scan_parquet(d / name / "**" / "*.parquet", hive_partitioning=True).drop("year")


def exotic_report(paths: Paths, hr: pl.DataFrame) -> str:
    """O2〜O6 の確定オッズと HR の払戻。的中組番が 1 つのレースで payout = オッズ × 100 か。

    ワイドは的中組番が 3 つあり（同着がなければ）、払戻はその組番の最低〜最高オッズの間に入るはずなので、それを数える。
    """
    d = paths.out
    out = ["## odds_final_quinella〜trifecta（O2〜O6 確定オッズ）と HR の払戻\n"]
    rows, cover = [], []
    for name, bet in EXOTIC_NAMES:
        lf = _scan_table(d, name)
        odds_cols = ["odds_min", "odds_max"] if bet == "wide" else ["odds"]
        o = lf.select("race_key", "combination", *odds_cols, "status").collect()
        per_race = o.group_by("race_key").agg(n=pl.len())
        st = o["status"].value_counts()
        st = dict(zip(st["status"].cast(pl.String), st["count"]))
        pay = hr.filter(pl.col("bet_type") == bet)
        n_win = pay.group_by("race_key").agg(nw=pl.len())
        if bet == "wide":
            # 3 着の同着があると的中組番が 5 つ以上になり、払戻は最低オッズより低くなる。3 つのレースだけで比べる
            three = pay.join(n_win.filter(pl.col("nw") == 3), on="race_key", how="semi")
            j = three.join(o, on=["race_key", "combination"], how="inner").drop_nulls("odds_min")
            lo, hi = (pl.col("odds_min") * 100).round(0), (pl.col("odds_max") * 100).round(0)
            ok = j.filter((pl.col("payout") >= lo) & (pl.col("payout") <= hi)).height
            target = j.height
        else:
            single = pay.join(n_win.filter(pl.col("nw") == 1), on="race_key", how="semi")
            j = single.join(o, on=["race_key", "combination"], how="inner").drop_nulls("odds")
            ok = j.filter(pl.col("payout") == (pl.col("odds") * 100).round(0)).height
            target = j.height
        pay_races = pay["race_key"].n_unique()
        no_odds = pay.join(per_race, on="race_key", how="anti")["race_key"].n_unique()
        rows.append((bet, o.height, per_race.height, f"{o['race_key'].min()[:8]}〜{o['race_key'].max()[:8]}",
                     int(per_race["n"].max()), target, ok, f"{100 * ok / target:.2f}%" if target else "-",
                     pay_races, no_odds))
        cover.append(f"- {bet}: status {st}")
        if bet == "wide":
            cover.append(f"  - 同着で的中組番が 4 つ以上のワイドのレース: {n_win.filter(pl.col('nw') > 3).height}（比べていない）。")
    out.append("- 一致の条件: 馬連・馬単・3連複・3連単は、的中組番が 1 つのレースで payout = round(オッズ × 100)。"
               "ワイドは的中組番が 3 つのレースで round(最低オッズ × 100) <= payout <= round(最高オッズ × 100)。"
               "オッズが null（ok 以外）の組番は除く。\n")
    out.append(_md(pl.DataFrame(rows, orient="row", schema=[
        "bet_type", "rows", "races", "period", "max_combos", "compared", "match", "match_pct",
        "payout_races", "payout_races_without_odds"])) + "\n")
    out.extend(cover)
    # 一致しない例の内訳（レース数・年）
    for name, bet in EXOTIC_NAMES:
        if bet == "wide":
            continue
        o = _scan_table(d, name).select("race_key", "combination", "odds").collect()
        pay = hr.filter(pl.col("bet_type") == bet)
        single = pay.join(pay.group_by("race_key").agg(nw=pl.len()).filter(pl.col("nw") == 1), on="race_key",
                          how="semi")
        j = single.join(o, on=["race_key", "combination"]).drop_nulls("odds").with_columns(
            exp=(pl.col("odds") * 100).round(0))
        bad = j.filter(pl.col("payout") != pl.col("exp"))
        if bad.height:
            yrs = dict(sorted(bad.group_by(pl.col("race_key").str.slice(0, 4)).len().iter_rows()))
            out.append(f"- {bet} の不一致 {bad.height} 行: 年 {yrs}、特払 {int((bad['special_payout'] == 1).sum())}、"
                       f"オッズの最大値（{bad['odds'].max()}）の行 {int((bad['odds'] == bad['odds'].max()).sum())}、"
                       f"payout / (オッズ × 100) の中央値 {(bad['payout'] / bad['exp']).median():.3f}。")
    out.append("")
    return "\n".join(out)


def snap_report(paths: Paths, ra: pl.DataFrame) -> str:
    d = paths.out
    out = ["## odds_ts_quinella_snap（0B42 馬連の発走前スナップショット）\n"]
    state = json.loads((paths.stage / "_state_odds_ts_quinella_snap.json").read_text())
    tot: dict[str, int] = {}
    for v in state.values():
        for k, x in v["stats"].items():
            tot[k] = tot.get(k, 0) + x
    out.append(f"- 取り込み: ファイル {tot.get('files', 0):,}（空 {tot.get('empty_files', 0)}）、"
               f"レコード（発表） {tot.get('records', 0):,}、長さ不正 {tot.get('bad_length', 0)}、"
               f"ファイル名とキーの不一致 {tot.get('key_mismatch', 0)}、同じ分の重複発表 {tot.get('duplicate_records', 0):,}"
               f"（票数の多い方を残した）、中間の発表時刻を読めない {tot.get('mdhm_unparsed', 0)}、"
               f"races に発走時刻がないレース {tot.get('races_without_post_at', 0)}、行 {tot.get('rows', 0):,}。")
    sn = pl.scan_parquet(d / "odds_ts_quinella_snap" / "**" / "*.parquet", hive_partitioning=True)
    recs = sn.group_by("race_key", "snap").agg(pl.col("announced_at").first(), pl.col("data_kubun").first(),
                                               n=pl.len()).collect()
    held = ra.filter(~pl.col("is_cancelled") & (pl.col("date") >= pl.date(2003, 10, 1)))
    cov = held.select("race_key", "year", "post_at")
    for s in ("1", "5", "10", "60", "last"):
        cov = cov.join(recs.filter(pl.col("snap") == s).select("race_key", pl.lit(True).alias(f"has_{s}")),
                       on="race_key", how="left")
    by = cov.group_by("year").agg(
        races=pl.len(), **{f"snap_{s}": pl.col(f"has_{s}").is_not_null().sum() for s in ("1", "5", "10", "60", "last")}
    ).sort("year").with_columns(cov_10=pl.col("snap_10") / pl.col("races"))
    out.append(f"- 2003-10 以降の開催レースのうちスナップショットがあるもの（last）: "
               f"{_pct(int(by['snap_last'].sum()), int(by['races'].sum()))}、10 分前: "
               f"{_pct(int(by['snap_10'].sum()), int(by['races'].sum()))}。")
    out.append(f"- races にないレース: {recs.join(ra, on='race_key', how='anti')['race_key'].n_unique()}。")
    out.append("- 年ごとの、各スナップショットがあるレース数:\n")
    out.append(_md(by) + "\n")
    lead = recs.filter(pl.col("snap") != "last").join(ra.select("race_key", "post_at"), on="race_key").with_columns(
        lead=(pl.col("post_at") - pl.col("announced_at")).dt.total_minutes())
    lt = lead.group_by("snap").agg(median=pl.col("lead").median(), p90=pl.col("lead").quantile(0.9),
                                   max=pl.col("lead").max(), races=pl.len())
    lt = lt.sort(pl.col("snap").cast(pl.Int32))
    out.append("- スナップショットの発表が発走の何分前か（分）:\n")
    out.append(_md(lt) + "\n")
    l1 = lead.filter(pl.col("snap") == "1").with_columns(year=pl.col("race_key").str.slice(0, 4))
    l1 = l1.group_by("year").agg(races=pl.len(), median=pl.col("lead").median(),
                                 ge5=(pl.col("lead") >= 5).mean()).sort("year")
    out.append("- snap 1（発走前の最後の中間オッズ）が発走の何分前か（年ごと）:\n")
    out.append(_md(l1) + "\n")
    cancelled = recs.filter(pl.col("snap") == "last").join(ra.filter(pl.col("is_cancelled")), on="race_key", how="semi")
    out.append(f"- 中止のレース（races の is_cancelled）のスナップショット: {cancelled.height} レース。")
    last_kb = recs.filter(pl.col("snap") == "last")["data_kubun"].value_counts()
    out.append(f"- last の発表のデータ区分: {dict(sorted(last_kb.iter_rows()))}")
    # last と確定オッズ
    last = sn.filter(pl.col("snap") == "last").select("race_key", "combination", "data_kubun",
                                                      ts="odds").collect()
    o2 = pl.read_parquet(d / "odds_final_quinella.parquet", columns=["race_key", "combination", "odds"])
    j = last.join(o2, on=["race_key", "combination"], how="inner")
    both = j.filter(pl.col("ts").is_not_null() & pl.col("odds").is_not_null())
    eq = both.filter((pl.col("ts") - pl.col("odds")).abs() < 0.05)
    out.append(f"- last と O2（確定）の馬連オッズ: 一致 {_pct(eq.height, both.height)}。"
               f"片方だけ値がある組番 {j.height - both.height - j.filter(pl.col('ts').is_null() & pl.col('odds').is_null()).height}。")
    bad = both.join(eq, on=["race_key", "combination"], how="anti")
    out.append(f"  - 一致しない組番を含むレース: {bad['race_key'].n_unique()}"
               f"（そのレースの last のデータ区分 {dict(sorted(bad.group_by('race_key').agg(pl.col('data_kubun').first())['data_kubun'].value_counts().iter_rows()))}）。")
    lr = last["race_key"].unique()
    o2r = o2.filter(pl.col("race_key") >= "20031001")["race_key"].unique()
    out.append(f"  - last があって O2 がないレース: {int((~lr.is_in(o2['race_key'].unique())).sum())}。"
               f"O2 があって last がない 2003-10 以降のレース: {int((~o2r.is_in(lr)).sum())}。\n")
    return "\n".join(out)


def ts_report(paths: Paths, ra: pl.DataFrame, o1: pl.DataFrame) -> str:
    out: list[str] = ["## odds_ts_win（0B41 時系列オッズ）\n"]
    ts = pl.scan_parquet(paths.out / "odds_ts_win" / "**" / "*.parquet", hive_partitioning=True)
    state = json.loads((paths.stage / "_state_odds_ts.json").read_text())
    tot: dict[str, int] = {}
    for v in state.values():
        for k, x in v["stats"].items():
            tot[k] = tot.get(k, 0) + x
    out.append(f"- 取り込み: ファイル {tot.get('files', 0):,}、レコード（発表） {tot.get('records', 0):,}、"
               f"長さ不正 {tot.get('bad_length', 0)}、ファイル名とキーの不一致 {tot.get('key_mismatch', 0)}、"
               f"同じ分の重複発表 {tot.get('duplicate_records', 0):,}（票数の多い方を残した）、"
               f"発表時刻を読めない {tot.get('mdhm_unparsed', 0)}、行 {tot.get('rows', 0):,}。")
    snaps = (ts.group_by("race_key", "announced_at", "data_kubun")
             .agg(n=pl.len()).collect())
    out.append(f"- データ区分ごとの発表数: {dict(sorted(snaps['data_kubun'].value_counts().iter_rows()))}")
    per = snaps.group_by("race_key").agg(n=pl.len(), n_mid=(pl.col("data_kubun") == "1").sum())
    out.append(f"- 1 レースあたりの発表数: 中央値 {per['n'].median():.0f}、平均 {per['n'].mean():.1f}、"
               f"最小 {per['n'].min()}、最大 {per['n'].max()}。")
    held = ra.filter(~pl.col("is_cancelled") & (pl.col("date") >= pl.date(2003, 10, 1)))
    cov = held.join(per, on="race_key", how="left")
    out.append(f"- 2003-10 以降の開催レースのうち時系列があるもの: {_pct(cov['n'].is_not_null().sum(), cov.height)}。")
    extra = per.join(ra, on="race_key", how="anti").height
    out.append(f"- races にないレースの時系列: {extra}。")

    # 発走時刻との関係
    s = snaps.join(ra.select("race_key", "post_at", "year"), on="race_key", how="inner").with_columns(
        lead=(pl.col("post_at") - pl.col("announced_at")).dt.total_minutes())
    after = s.filter(pl.col("lead") < 0).group_by("data_kubun").agg(n=pl.len()).sort("data_kubun")
    out.append(f"- 発走時刻より後の発表（データ区分ごと）: {dict(after.iter_rows())}"
               f"（中間 1 の発走後の発表は {int(after.filter(pl.col('data_kubun') == '1')['n'].sum())}）。")
    mid = s.filter(pl.col("data_kubun") == "1")
    lead = mid.group_by("race_key", "year").agg(
        best=pl.col("lead").filter(pl.col("lead") >= 0).min(), first=pl.col("lead").max())
    rows = []
    for th in (1, 2, 5, 10, 30):
        rows.append((f">= {th} 分前", int((lead["first"] >= th).sum()), int((lead["best"] >= th).sum()), lead.height))
    out.append("- 中間オッズ（データ区分 1）のあるレースのうち、"
               "発走 N 分以上前の発表が 1 つでもあるもの（any）と、発走前の最後の発表が N 分以上前のもの（last）:\n")
    out.append(_md(pl.DataFrame(rows, schema=["条件", "any", "last", "of"], orient="row")) + "\n")
    out.append(f"- 最初の中間オッズは発走の {lead['first'].median():.0f} 分前（中央値）、最小 {lead['first'].min()} 分前。")
    out.append("- 発走前の最後の中間オッズが発走の何分前か（年ごと、分）:\n")
    out.append(_md(lead.group_by("year").agg(
        races=pl.len(), median=pl.col("best").median(), p90=pl.col("best").quantile(0.9),
        ge5=(pl.col("best") >= 5).mean(), ge10=(pl.col("best") >= 10).mean()).sort("year")) + "\n")

    # 最後の発表 vs O1 確定
    last_at = ts.group_by("race_key").agg(_m=pl.col("announced_at").max())
    last = (ts.join(last_at, on="race_key").filter(pl.col("announced_at") == pl.col("_m"))
            .select("race_key", "umaban", "data_kubun", ts_odds="win_odds")).collect()
    j = last.join(o1.select("race_key", "umaban", "win_odds"), on=["race_key", "umaban"], how="inner")
    both = j.filter(pl.col("ts_odds").is_not_null() & pl.col("win_odds").is_not_null())
    eq = both.filter((pl.col("ts_odds") - pl.col("win_odds")).abs() < 0.05)
    out.append("- 各レースの最後の発表と O1（確定）の単勝オッズ:")
    out.append(f"  - 一致: {_pct(eq.height, both.height)}。最後の発表のデータ区分: "
               f"{dict(sorted(last.group_by('race_key').agg(pl.col('data_kubun').first())['data_kubun'].value_counts().iter_rows()))}")
    rk_bad = both.join(eq, on=["race_key", "umaban"], how="anti")["race_key"].n_unique()
    out.append(f"  - 一致しない馬を含むレース: {rk_bad}。")
    # 発走 5 分前の最後の中間オッズと確定オッズの差
    pre = mid.filter(pl.col("lead") >= 5).group_by("race_key").agg(pl.col("announced_at").max())
    pre_odds = ts.join(pre.lazy(), on=["race_key", "announced_at"]).filter(pl.col("data_kubun") == "1") \
        .select("race_key", "umaban", pre="win_odds").collect()
    pj = pre_odds.join(o1.select("race_key", "umaban", "win_odds"), on=["race_key", "umaban"]).drop_nulls()
    pj = pj.with_columns(r=(pl.col("pre").log() - pl.col("win_odds").log()).abs())
    out.append(f"- 発走 5 分以上前の最後の中間オッズと確定オッズ: |log 比| の中央値 {pj['r'].median():.3f}、"
               f"平均 {pj['r'].mean():.3f}、一致 {_pct(int((pj['r'] < 1e-6).sum()), pj.height)}。\n")
    return "\n".join(out)
