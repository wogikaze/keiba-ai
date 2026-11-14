import polars as pl
from polars.testing import assert_frame_equal

from keiba_ai import features_rating as FR
from test_features_hist2 import _data, _write


def test_rating_uses_only_previous_days(tmp_path):
    races, ents, horses = _data(1)
    mid = sorted(races["date"].unique())[15]
    rk_mid = races.filter(pl.col("date") == mid)["race_key"]
    ents2 = ents.with_columns(finish_pos=pl.when(pl.col("race_key").is_in(rk_mid.implode()))
                              .then(9 - pl.col("finish_pos")).otherwise("finish_pos"))
    _write(tmp_path / "a", races, ents, horses)
    _write(tmp_path / "b", races, ents2, horses)
    fa = FR.load_rating(tmp_path / "a").sort("race_key", "umaban")
    fb = FR.load_rating(tmp_path / "b").sort("race_key", "umaban")
    dates = fa.join(races.select("race_key", "date"), on="race_key")["date"]
    upto = (dates <= mid).to_numpy()
    assert_frame_equal(fa.filter(upto), fb.filter(upto))
    assert not fa.filter(~upto).equals(fb.filter(~upto))
    # 初出走は初期値
    assert fa["rt_elo"].min() <= FR.R0 <= fa["rt_elo"].max()
