"""docs/literature/*.md の frontmatter を検査する。

使い方: uv run python scripts/check_literature.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIT = ROOT / "docs" / "literature"
REQUIRED = ["title", "authors", "year", "topic", "verified", "importance"]
ENUMS = {
    "verified": {"fulltext", "abstract", "metadata"},
    "importance": {"high", "medium", "low"},
    "source": {"downloaded", "transcribed", "unavailable"},
}
# library/ はローカル専用なので、無い環境（CI など）では原本の存在チェックを省く
LIB_PRESENT = (ROOT / "library").is_dir()
NAME_RE = re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*\.md$")


def frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def main() -> int:
    errors: list[str] = []
    titles: Counter[str] = Counter()
    topics: Counter[str] = Counter()
    for f in sorted(LIT.glob("*.md")):
        if f.name.startswith("_"):
            continue
        if not NAME_RE.match(f.name):
            errors.append(f"{f.name}: ファイル名が規約外")
        fm = frontmatter(f.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{f.name}: frontmatter なし")
            continue
        for k in REQUIRED:
            if not fm.get(k):
                errors.append(f"{f.name}: {k} が空")
        for k, allowed in ENUMS.items():
            if fm.get(k) and fm[k] not in allowed:
                errors.append(f"{f.name}: {k}={fm[k]} は {sorted(allowed)} のどれでもない")
        lib = ROOT / "library" / f.stem
        if fm.get("source") in {"downloaded", "transcribed"} and LIB_PRESENT and not (lib / "source.txt").exists():
            errors.append(f"{f.name}: source={fm['source']} だが library/{f.stem}/source.txt がない")
        if not fm.get("url") and not fm.get("doi"):
            errors.append(f"{f.name}: url も doi もない")
        titles[re.sub(r"\W+", "", fm.get("title", "").lower())] += 1
        topics[fm.get("topic", "?")] += 1
    for t, n in titles.items():
        if t and n > 1:
            errors.append(f"タイトル重複の疑い: {t[:60]} ({n}件)")
    print("topic別:", dict(topics), "合計", sum(topics.values()))
    for e in errors:
        print("NG", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
