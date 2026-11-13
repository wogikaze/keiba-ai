"""固定長レコードを numpy の 2 次元配列にして、列ごとにまとめて切り出す。

1 行ずつ Python で切るのは遅いので、同じ種別の行を (行数, レコード長) の uint8 配列に詰め、
項目はその列範囲として取り出す。数値は桁ごとの演算で変換し、数字でない値（空白、`----` など）は欠損にする。
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np

from .layout import Field, Layout

_D0, _D9, _SP = ord("0"), ord("9"), ord(" ")


def read_records(path: Path, types: Iterable[str]) -> dict[str, list[bytes]]:
    """ファイルを 1 行ずつ読み、先頭 2 バイトのレコード種別ごとに行を集める。"""
    want = {t.encode() for t in types}
    out: dict[str, list[bytes]] = {t: [] for t in types}
    with open(path, "rb", buffering=1 << 22) as f:
        for line in f:
            t = line[:2]
            if t in want:
                out[t.decode()].append(line.rstrip(b"\r\n"))
    return out


class Batch:
    """同じレコード種別の行の集まり。"""

    def __init__(self, layout: Layout, lines: list[bytes]):
        self.layout = layout
        n, width = len(lines), layout.length
        # 長さの合わない行は数えておき、右を空白で埋めるか切って揃える
        self.bad_length = sum(len(x) != width for x in lines)
        buf = b"".join(x.ljust(width)[:width] for x in lines)
        self.mat = np.frombuffer(buf, dtype=np.uint8).reshape(n, width) if n else np.zeros((0, width), np.uint8)

    def __len__(self) -> int:
        return self.mat.shape[0]

    def take(self, idx: np.ndarray) -> Batch:
        b = object.__new__(Batch)
        b.layout, b.bad_length, b.mat = self.layout, 0, self.mat[idx]
        return b

    def _field(self, name: str | Field) -> Field:
        return name if isinstance(name, Field) else self.layout[name]

    def _cols(self, f: Field, i: int | None) -> np.ndarray:
        """(n, length) の部分配列。i が None なら全要素を (n, count, length) で返す。"""
        offs = f.offsets()
        if i is not None:
            o = offs[i]
            return self.mat[:, o : o + f.length]
        idx = np.asarray(offs)[:, None] + np.arange(f.length)[None, :]
        return self.mat[:, idx]

    def raw(self, name: str | Field, i: int | None = 0) -> np.ndarray:
        """バイト列のまま（numpy の S 型）。"""
        f = self._field(name)
        a = np.ascontiguousarray(self._cols(f, i))
        return a.view(f"S{f.length}").reshape(a.shape[:-1])

    def str(self, name: str | Field, i: int | None = 0) -> np.ndarray:
        """ASCII の項目を文字列にする（末尾の空白は numpy が残す。前後の空白を除く）。"""
        r = self.raw(name, i)
        return np.char.strip(np.char.decode(r, "ascii", errors="replace"))

    def text(self, name: str | Field, i: int | None = 0) -> list[str]:
        """全角を含む項目を cp932 で読み、前後の空白（全角を含む）を除く。"""
        r = self.raw(name, i)
        return [x.decode("cp932", errors="replace").strip() for x in r.tolist()]

    def num(self, name: str | Field, i: int | None = 0, scale: float = 1.0, signed: bool = False) -> np.ndarray:
        """数字の項目を float64 にする。数字として読めない値は NaN。

        前に空白があるのは許す（右詰め）。すべて空白、途中に空白や記号があれば NaN。
        signed=True なら先頭 1 バイトの `+` / `-` / 空白を符号として読む。
        """
        a = self._cols(self._field(name), i).astype(np.int16)
        sign = None
        if signed:
            head = a[..., 0]
            sign = np.where(head == ord("-"), -1.0, 1.0)
            ok_sign = (head == ord("-")) | (head == ord("+")) | (head == _SP)
            a = a[..., 1:]
        isdig = (a >= _D0) & (a <= _D9)
        isspace = a == _SP
        seen = np.cumsum(isdig, axis=-1) > 0
        valid = (isdig | (isspace & ~seen)).all(axis=-1) & isdig.any(axis=-1)
        if signed:
            valid &= ok_sign
        digits = np.where(isdig, a - _D0, 0).astype(np.int64)
        pw = 10 ** np.arange(a.shape[-1] - 1, -1, -1, dtype=np.int64)
        v = (digits * pw).sum(axis=-1).astype(np.float64)
        if sign is not None:
            v *= sign
        v = np.where(valid, v * scale, np.nan)
        return v
