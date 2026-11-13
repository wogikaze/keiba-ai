"""JV-Data仕様書「フォーマット」シート（CSV）からレコードレイアウトを作る。

オフセットは手で書かず、すべてここで仕様書から読む。
位置は 0 始まりのバイト位置に直す。行末の CR/LF（レコード区切）は取り込み時に落としてあるので、
レコード長は仕様書の値から 2 を引いた長さになる。
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_SPEC = Path("data/raw/jra-van/specs/text/JV-Data仕様書__フォーマット.csv")

_ID_RE = re.compile(r'"([0-9A-Z]{2})"')
_POS_RE = re.compile(r"^\(?\s*(\d+)\s*\)?$")


def normalize(name: str) -> str:
    """項目名から空白（全角を含む）と <> を除く。"""
    return re.sub(r"[\s　<>]", "", name)


@dataclass(frozen=True)
class Field:
    """1 つの項目。繰返しがあれば offsets() が全要素の開始位置を返す。

    group 内の項目は、group の繰返し（outer）と項目自身の繰返し（inner）の 2 段を持てる。
    """

    name: str
    start: int  # 0 始まり。最初の要素の位置
    length: int  # 1 要素のバイト数
    outer: int = 1  # group の繰返し回数（group 外なら項目自身の繰返し）
    outer_stride: int = 0
    inner: int = 1  # group 内項目自身の繰返し
    group: str | None = None

    @property
    def count(self) -> int:
        return self.outer * self.inner

    def offsets(self) -> list[int]:
        return [
            self.start + o * self.outer_stride + i * self.length
            for o in range(self.outer)
            for i in range(self.inner)
        ]


@dataclass
class Layout:
    record_id: str
    title: str
    length: int  # CR/LF を除いたレコード長
    fields: dict[str, Field] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Field:
        """`項目名` か `グループ名.項目名`（いずれも normalize 後）で引く。"""
        try:
            return self.fields[key]
        except KeyError:
            raise KeyError(f"{self.record_id}: 項目 {key!r} がない。候補: {list(self.fields)[:80]}") from None


def _int(s: str) -> int | None:
    s = s.strip()
    return int(s) if s.isdigit() else None


def parse_format_csv(text: str) -> dict[str, Layout]:
    """フォーマット CSV の本文からレコード種別 ID → Layout を作る。"""
    layouts: dict[str, Layout] = {}
    cur: Layout | None = None
    group: tuple[str, int, int, int] | None = None  # (名前, 開始, 繰返, 1 回分のバイト数)
    for row in csv.reader(io.StringIO(text)):
        row = row + [""] * (11 - len(row))
        no, sub, name, pos, rep, size, total = row[1], row[2], row[4], row[5], row[6], row[7], row[8]
        if pos.strip() == "レコード長":
            cur = Layout(record_id="", title=no.strip(), length=int(size) - 2)
            group = None
            continue
        if cur is None:
            continue
        p = _POS_RE.match(pos.strip())
        if not p or _int(size) is None:
            continue  # 見出し行・注記行
        start, nbytes, nrep = int(p.group(1)), int(size), _int(rep) or 1
        nm = normalize(name)
        if no.strip() == "1" and not sub.strip():
            m = _ID_RE.search(row[10])
            if m:
                cur.record_id = m.group(1)
                layouts[cur.record_id] = cur
        is_child = bool(sub.strip()) or pos.strip().startswith("(")
        if is_child and group is not None:
            gname, gstart, grep, gsize = group
            f = Field(nm, gstart + start - 1, nbytes, grep, gsize, nrep, gname)
            key = f"{gname}.{nm}"
        elif name.strip().startswith("<"):
            group = (nm, start - 1, nrep, nbytes)
            continue
        else:
            group = None
            f = Field(nm, start - 1, nbytes, nrep, nbytes)
            key = nm
            if nm == "レコード区切":
                continue
        while key in cur.fields:  # 「予備」など同名の項目
            key += "_"
        cur.fields[key] = f
    return layouts


def load_layouts(path: Path | str = DEFAULT_SPEC) -> dict[str, Layout]:
    return parse_format_csv(Path(path).read_text(encoding="utf-8"))


def check_layout(layout: Layout) -> list[str]:
    """項目が重ならずレコード長に収まるかを調べ、問題の一覧を返す。"""
    spans = sorted((o, o + f.length, k) for k, f in layout.fields.items() for o in f.offsets())
    problems = []
    end = 0
    for s, e, k in spans:
        if s < end:
            problems.append(f"{k} が前の項目と重なる（{s} < {end}）")
        end = max(end, e)
    if end != layout.length:
        problems.append(f"項目の終わり {end} がレコード長 {layout.length} と合わない")
    return problems
