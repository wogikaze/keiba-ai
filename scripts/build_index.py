"""experiments/*/results.json から experiments/INDEX.md（リーダーボード）を生成する。

使い方: uv run python scripts/build_index.py [--sort-by METRIC] [--desc]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = ROOT / "experiments"
INDEX = EXP_DIR / "INDEX.md"


def read_title(readme: Path) -> str:
    if not readme.exists():
        return ""
    text = readme.read_text(encoding="utf-8")
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def load_experiments() -> list[dict]:
    rows = []
    for d in sorted(EXP_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")):
            continue
        rj = d / "results.json"
        res = json.loads(rj.read_text(encoding="utf-8")) if rj.exists() else {}
        rows.append({"name": d.name, "title": read_title(d / "README.md"), **res})
    return rows


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def render(rows: list[dict], sort_by: str | None, desc: bool) -> str:
    metric_keys = sorted({k for r in rows for k in (r.get("metrics") or {})})
    if sort_by:
        def key(r):
            v = (r.get("metrics") or {}).get(sort_by)
            return (v is None, -v if (desc and v is not None) else v)
        rows = sorted(rows, key=key)
    else:
        rows = sorted(rows, key=lambda r: r["name"], reverse=True)

    head = ["experiment", "title", "status", *metric_keys, "split", "data", "seed", "git"]
    lines = [
        "---",
        "title: 実験リーダーボード",
        "---",
        "",
        "# 実験リーダーボード",
        "",
        "> このファイルは `scripts/build_index.py` で自動生成される。手で編集しないこと。",
        "",
        "| " + " | ".join(head) + " |",
        "| " + " | ".join("---" for _ in head) + " |",
    ]
    for r in rows:
        m = r.get("metrics") or {}
        git = (r.get("git_hash") or "")[:7] or "-"
        cells = [
            f"[{r['name']}](./{r['name']}/README.md)",
            r["title"] or "-",
            fmt(r.get("status")),
            *(fmt(m.get(k)) for k in metric_keys),
            fmt(r.get("split")),
            fmt(r.get("data_version")),
            fmt(r.get("seed")),
            f"`{git}`" if git != "-" else "-",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sort-by", help="並べ替えに使う metrics のキー")
    p.add_argument("--desc", action="store_true", help="降順（大きいほど良い指標）")
    a = p.parse_args()
    INDEX.write_text(render(load_experiments(), a.sort_by, a.desc), encoding="utf-8")
    print(f"wrote {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
