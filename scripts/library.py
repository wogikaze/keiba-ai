"""先行研究の原本ライブラリ（library/、gitignore）を扱う。

library/<ノートのslug>/
  source.pdf | source.html   取得した原本
  source.txt                 文字起こし。PDF は "=== page N ===" で区切る
  meta.json                  取得元URL・日時・sha256・抽出方法など

使い方:
  uv run python scripts/library.py fetch <slug> <url> [--kind pdf|html]
  uv run --extra browser python scripts/library.py fetch <slug> <url> --browser   # 自動取得が拒否されるとき
  uv run python scripts/library.py add <slug> <手元のPDF> --url <入手元> --version published  # 手動DLした原本
  uv run python scripts/library.py extract <slug>        # 原本から source.txt を作り直す
  uv run --extra ocr python scripts/library.py ocr [<slug>]   # スキャン画像PDFを OCR
  uv run python scripts/library.py attach <slug> <名前> <url> --description "..."  # 二次資料を添付
  uv run python scripts/library.py mark <slug> unavailable --reason "..."  # 取得できなかった記録
  uv run python scripts/library.py search <語> [<語> ...] [-C 1] [--topic X]
  uv run python scripts/library.py status
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
LIT = ROOT / "docs" / "literature"
UA = "Mozilla/5.0 (X11; Linux x86_64) keiba-ai-research/0.1"
# 1ページあたりの文字数がこれ未満ならスキャン画像PDFとみなす
MIN_CHARS_PER_PAGE = 200


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def frontmatter(path: Path) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    fm: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def note_path(slug: str) -> Path:
    p = LIT / f"{slug}.md"
    if not p.exists():
        sys.exit(f"ノートがない: {p.relative_to(ROOT)}")
    return p


def load_meta(d: Path) -> dict:
    f = d / "meta.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def save_meta(d: Path, meta: dict) -> None:
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------- 抽出 ----------

def is_garbled(text: str) -> bool:
    """テキスト層が文字化けしているか（フォントの符号化が壊れた PDF など）。"""
    body = re.sub(r"=== page \d+ ===|\s", "", text)
    if not body:
        return True
    n = len(body)
    alnum = sum(1 for c in body if c.isalnum())
    # CJK 拡張A（U+3400-4DBF）が多いのは、日本語フォントの誤デコードの典型
    ext_a = sum(1 for c in body if 0x3400 <= ord(c) <= 0x4DBF)
    bad = body.count("(cid:") + body.count("\ufffd") + sum(1 for c in body if 0xE000 <= ord(c) <= 0xF8FF)
    return alnum / n < 0.5 or ext_a / n > 0.01 or bad / n > 0.02


def extract_pdf(pdf: Path) -> tuple[str, dict]:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    pages = int(m.group(1)) if m else 0
    parts, chars = [], 0
    for i in range(1, pages + 1):
        t = subprocess.run(
            ["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(pdf), "-"],
            capture_output=True, text=True,
        ).stdout
        chars += len(t.strip())
        parts.append(f"=== page {i} ===\n{t.rstrip()}\n")
    text = "\n".join(parts)
    needs_ocr = pages > 0 and (chars / pages < MIN_CHARS_PER_PAGE or is_garbled(text))
    return text, {"pages": pages, "chars": chars, "method": "pdftotext -layout", "needs_ocr": needs_ocr}


def extract_html(html: Path) -> tuple[str, dict]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "form"]):
        tag.decompose()
    root = soup.find("article") or soup.find("main") or soup.body or soup
    lines = []
    for el in root.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th", "pre", "blockquote", "figcaption"]):
        if el.find_parent(["p", "li", "td", "th", "pre", "blockquote"]) is not None and el.name != "pre":
            continue
        text = " ".join(el.get_text(" ", strip=True).split())
        if not text:
            continue
        prefix = "#" * int(el.name[1]) + " " if el.name in {"h1", "h2", "h3", "h4"} else ""
        lines.append(prefix + text)
    text = "\n\n".join(lines)
    method = "beautifulsoup"
    # p/li などで組まれていないページ（Scribd のビューアなど）は、本文テキストをそのまま取る
    full = "\n".join(l.strip() for l in root.get_text("\n").splitlines() if l.strip())
    if len(text) < 0.3 * len(full):
        text, method = full, "beautifulsoup (get_text fallback)"
    return text + "\n", {"chars": len(text), "method": method, "needs_ocr": False}


def extract(d: Path) -> dict:
    pdf, html = d / "source.pdf", d / "source.html"
    if pdf.exists():
        text, info = extract_pdf(pdf)
    elif html.exists():
        text, info = extract_html(html)
    else:
        sys.exit(f"原本がない: {d}")
    (d / "source.txt").write_text(text, encoding="utf-8")
    return info


# ---------- OCR（スキャン画像PDF） ----------

def order_boxes(boxes: list[tuple[float, float, float, float, str]], width: float) -> list[str]:
    """OCR の行ボックスを読み順に並べる。2段組みに対応する。

    ページ幅の 60% を超える行（タイトル・段抜きの図表）で縦に区切り、
    区切りの間では行の左端 x から段を推定して、左の段から順に並べる。
    """
    boxes = sorted(boxes, key=lambda b: b[1])
    out: list[str] = []
    band: list[tuple[float, float, float, float, str]] = []

    def flush() -> None:
        if not band:
            return
        # 行の左端 x を並べ、ページ幅の 10% 以上の隙間で段に分ける（3行以上ある段だけ採用）
        xs = sorted(b[0] for b in band)
        starts, cluster = [], [xs[0]]
        for x in xs[1:]:
            if x - cluster[-1] > width * 0.10:
                if len(cluster) >= 3:
                    starts.append(cluster[0])
                cluster = [x]
            else:
                cluster.append(x)
        if len(cluster) >= 3:
            starts.append(cluster[0])
        if len(starts) <= 1:
            out.extend(b[4] for b in sorted(band, key=lambda b: (round(b[1] / 8), b[0])))
        else:
            def col(b):
                c = 0
                for i, st in enumerate(starts):
                    if b[0] >= st - width * 0.02:
                        c = i
                return c
            out.extend(b[4] for b in sorted(band, key=lambda b: (col(b), b[1])))
        band.clear()

    for b in boxes:
        if b[2] - b[0] > width * 0.6:
            flush()
            out.append(b[4])
        else:
            band.append(b)
    flush()
    return out


def ocr_pdf(pdf: Path, dpi: int = 200) -> tuple[str, dict]:
    import tempfile

    from rapidocr import RapidOCR

    engine = RapidOCR()
    parts, chars = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), f"{tmp}/p"], check=True)
        pages = sorted(Path(tmp).glob("p-*.png"), key=lambda q: int(q.stem.split("-")[-1]))
        for i, img in enumerate(pages, 1):
            r = engine(str(img))
            boxes = []
            if r.boxes is not None:
                for box, txt in zip(r.boxes, r.txts):
                    xs, ys = [pt[0] for pt in box], [pt[1] for pt in box]
                    boxes.append((min(xs), min(ys), max(xs), max(ys), txt))
            from PIL import Image

            with Image.open(img) as im:
                width = im.width
            lines = order_boxes(boxes, width)
            text = "\n".join(lines)
            chars += len(text)
            parts.append(f"=== page {i} ===\n{text}\n")
            print(f"  ocr page {i}/{len(pages)}", file=sys.stderr)
    return "\n".join(parts), {"pages": len(parts), "chars": chars, "method": f"rapidocr (PP-OCR, {dpi}dpi, 2段組み並べ替え)", "needs_ocr": False, "ocr": True}


# ---------- コマンド ----------

BLOCK_MARKERS = ("just a moment", "access denied", "attention required", "are you a robot", "captcha",
                 "verify you are human", "request unsuccessful", "enable javascript and cookies")


def browser_get(url: str, wait_s: float = 8.0, headed: bool = False) -> tuple[bytes, str, str]:
    """実ブラウザ（Playwright + Chrome）で URL を開き、PDF か本文 HTML を返す。

    PDF の応答・ダウンロードを捕まえる。ボット確認ページが出たら少し待って再読込する。
    """
    from playwright.sync_api import sync_playwright

    pdfs: list[tuple[bytes, str]] = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", headless=not headed)
        except Exception:
            browser = p.chromium.launch(headless=not headed)
        ctx = browser.new_context(accept_downloads=True, locale="en-US")
        page = ctx.new_page()

        def on_response(resp):
            try:
                if "application/pdf" in (resp.headers.get("content-type") or ""):
                    pdfs.append((resp.body(), resp.url))
            except Exception:
                pass

        page.on("response", on_response)
        try:
            with page.expect_download(timeout=int(wait_s * 1000) + 30000) as dl_info:
                try:
                    page.goto(url, wait_until="load", timeout=60000)
                except Exception:
                    pass
                for _ in range(3):
                    page.wait_for_timeout(wait_s * 1000)
                    if pdfs:
                        break
                    title = (page.title() or "").lower()
                    text = (page.inner_text("body") or "").lower()[:2000] if page.query_selector("body") else ""
                    if not any(m in title or m in text for m in BLOCK_MARKERS):
                        break
                if not pdfs:
                    # PDF 直リンクがビューアで開かれた場合などは、同じ Cookie で取り直す
                    r = ctx.request.get(url, timeout=60000)
                    if r.body()[:5] == b"%PDF-":
                        pdfs.append((r.body(), r.url))
                if pdfs:
                    raise _Done()
                html = page.content()
                final = page.url
                raise _Done()
            body = dl_info.value.path().read_bytes()
            browser.close()
            return body, "download", dl_info.value.url
        except _Done:
            pass
        except Exception:
            pass
        browser.close()
    if pdfs:
        return pdfs[-1][0], "application/pdf", pdfs[-1][1]
    low = html.lower()
    if any(m in low[:5000] for m in BLOCK_MARKERS):
        raise RuntimeError("ボット確認ページから進めなかった")
    return html.encode("utf-8"), "text/html (browser)", final


class _Done(Exception):
    pass


def cmd_fetch(a) -> None:
    note_path(a.slug)
    d = LIB / a.slug
    d.mkdir(parents=True, exist_ok=True)
    if a.browser:
        try:
            body, ctype, final_url = browser_get(a.url, headed=a.headed)
        except RuntimeError:
            if a.headed or not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
                raise
            # ヘッドレスはボット確認で止まりやすい。画面ありで再試行する（WSLg などで表示される）
            print("  ヘッドレスで止まったので画面ありで再試行", file=sys.stderr)
            body, ctype, final_url = browser_get(a.url, headed=True)
    else:
        req = urllib.request.Request(a.url, headers={"User-Agent": UA, "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            ctype = r.headers.get("Content-Type", "")
            final_url = r.geturl()
    kind = a.kind or ("pdf" if body[:5] == b"%PDF-" else "html")
    if a.kind == "pdf" and body[:5] != b"%PDF-":
        sys.exit(f"PDF ではない応答（Content-Type: {ctype}）。ログインページや要約ページの可能性。")
    for old in ("source.pdf", "source.html"):
        (d / old).unlink(missing_ok=True)
    (d / f"source.{kind}").write_bytes(body)
    info = extract(d)
    meta = {
        "slug": a.slug,
        "status": "downloaded",
        "url": a.url,
        "final_url": final_url,
        "content_type": ctype,
        "kind": kind,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "fetched_at": now(),
        "fetched_with": "playwright" if a.browser else "urllib",
        **info,
    }
    if a.version:
        meta["version"] = a.version
    # 添付（二次資料）の記録は引き継ぐ
    old_meta = load_meta(d)
    if old_meta.get("attachments"):
        meta["attachments"] = old_meta["attachments"]
    save_meta(d, meta)
    warn = "  ※スキャン画像か文字化けの可能性: library.py ocr で OCR する" if info.get("needs_ocr") else ""
    print(f"ok {a.slug}: {kind} {len(body):,} bytes, {info.get('pages', '-')} pages, {info.get('chars'):,} chars{warn}")


def cmd_add(a) -> None:
    """手元のファイル（ブラウザで手動ダウンロードした PDF など）を原本として取り込む。"""
    note_path(a.slug)
    src = Path(a.file).expanduser()
    body = src.read_bytes()
    kind = "pdf" if body[:5] == b"%PDF-" else "html"
    d = LIB / a.slug
    d.mkdir(parents=True, exist_ok=True)
    for old in ("source.pdf", "source.html"):
        (d / old).unlink(missing_ok=True)
    (d / f"source.{kind}").write_bytes(body)
    info = extract(d)
    meta = load_meta(d)
    meta.pop("reason", None)
    meta.update({
        "slug": a.slug, "status": "downloaded", "url": a.url or "", "kind": kind, "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(), "fetched_at": now(), "added_from": "manual", **info,
    })
    if a.version:
        meta["version"] = a.version
    save_meta(d, meta)
    warn = "  ※スキャン画像か文字化けの可能性: library.py ocr で OCR する" if info.get("needs_ocr") else ""
    print(f"ok {a.slug}: {kind}, {info.get('pages', '-')} pages, {info.get('chars'):,} chars{warn}")
    print("ノートの frontmatter を source: downloaded に直し、原本に基づいて書き直すこと")


def cmd_attach(a) -> None:
    """ノートが二次資料として使った別文献を library/<slug>/attachments/ に保存する。"""
    note_path(a.slug)
    d = LIB / a.slug / "attachments"
    d.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(a.url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        body, ctype, final_url = r.read(), r.headers.get("Content-Type", ""), r.geturl()
    kind = "pdf" if body[:5] == b"%PDF-" else "html"
    src = d / f"{a.name}.{kind}"
    src.write_bytes(body)
    text, info = extract_pdf(src) if kind == "pdf" else extract_html(src)
    (d / f"{a.name}.txt").write_text(text, encoding="utf-8")
    meta = load_meta(LIB / a.slug)
    meta.setdefault("attachments", {})[a.name] = {
        "description": a.description, "url": a.url, "final_url": final_url, "content_type": ctype,
        "kind": kind, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "fetched_at": now(), **info,
    }
    save_meta(LIB / a.slug, meta)
    print(f"ok {a.slug}/attachments/{a.name}.{kind}: {info.get('pages', '-')} pages, {info.get('chars'):,} chars")


def cmd_extract(a) -> None:
    d = LIB / a.slug
    info = extract(d)
    meta = load_meta(d)
    meta.update(info)
    save_meta(d, meta)
    print(f"ok {a.slug}: {info}")


def cmd_ocr(a) -> None:
    targets = [a.slug] if a.slug else [
        m.parent.name for m in sorted(LIB.glob("*/meta.json"))
        if json.loads(m.read_text(encoding="utf-8")).get("needs_ocr")
    ]
    for slug in targets:
        d = LIB / slug
        pdf = d / "source.pdf"
        if not pdf.exists():
            print(f"skip {slug}: PDF がない")
            continue
        print(f"ocr {slug}")
        text, info = ocr_pdf(pdf)
        (d / "source.txt").write_text(text, encoding="utf-8")
        meta = load_meta(d)
        meta.update(info)
        meta["ocr_at"] = now()
        save_meta(d, meta)
        print(f"ok {slug}: {info['pages']} pages, {info['chars']:,} chars")


def cmd_mark(a) -> None:
    note_path(a.slug)
    d = LIB / a.slug
    d.mkdir(parents=True, exist_ok=True)
    meta = load_meta(d)
    meta.update({"slug": a.slug, "status": a.status, "reason": a.reason, "marked_at": now()})
    if a.method:
        meta["method"] = a.method
    save_meta(d, meta)
    print(f"ok {a.slug}: {a.status}")


def cmd_search(a) -> None:
    terms = [t.lower() for t in a.terms]
    topics = {p.stem: frontmatter(p) for p in LIT.glob("*.md")}
    hits = 0
    for txt in sorted([*LIB.glob("*/source.txt"), *LIB.glob("*/attachments/*.txt")]):
        slug = txt.parent.name if txt.name == "source.txt" else txt.parent.parent.name
        fm = topics.get(slug, {})
        if a.topic and fm.get("topic") != a.topic:
            continue
        lines = txt.read_text(encoding="utf-8").splitlines()
        page = None
        shown_header = False
        for i, line in enumerate(lines):
            m = re.match(r"^=== page (\d+) ===$", line)
            if m:
                page = int(m.group(1))
                continue
            low = line.lower()
            if not all(t in low for t in terms):
                continue
            if not shown_header:
                print(f"\n## {slug}  —  {fm.get('title', '')}")
                print(f"   note: docs/literature/{slug}.md   source: {txt.relative_to(ROOT)}")
                shown_header = True
            loc = f"p.{page} " if page else ""
            lo, hi = max(0, i - a.context), min(len(lines), i + a.context + 1)
            snippet = " / ".join(s.strip() for s in lines[lo:hi] if s.strip() and not s.startswith("=== page"))
            print(f"   [{loc}L{i + 1}] {snippet[:300]}")
            hits += 1
    print(f"\n{hits} 件")


def cmd_status(a) -> None:
    rows = []
    for p in sorted(LIT.glob("[0-9]*.md")):
        meta = load_meta(LIB / p.stem)
        st = meta.get("status", "missing")
        if st == "downloaded" and meta.get("needs_ocr") and not meta.get("transcribed"):
            st = "needs_ocr"
        rows.append((st, p.stem, meta.get("reason", "")))
    from collections import Counter
    c = Counter(r[0] for r in rows)
    print("集計:", dict(c), "合計", len(rows))
    if a.verbose:
        for st, slug, reason in rows:
            if st != "downloaded":
                print(f"{st:12} {slug}  {reason}")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("slug")
    f.add_argument("url")
    f.add_argument("--kind", choices=["pdf", "html"])
    f.add_argument("--version", help="例: published / accepted-manuscript / preprint / working-paper")
    f.add_argument("--browser", action="store_true", help="実ブラウザ（Playwright）で取得する。要 uv sync --extra browser")
    f.add_argument("--headed", action="store_true", help="--browser で画面を表示する（WSLg など）")
    f.set_defaults(func=cmd_fetch)
    ad = sub.add_parser("add", help="手動ダウンロードしたファイルを原本として取り込む")
    ad.add_argument("slug")
    ad.add_argument("file")
    ad.add_argument("--url", help="入手元のURL")
    ad.add_argument("--version")
    ad.set_defaults(func=cmd_add)
    at = sub.add_parser("attach", help="二次資料（原本以外の文献）をノートに添付する")
    at.add_argument("slug")
    at.add_argument("name", help="ファイル名（例: jullien-salanie-2005-idei-wp）")
    at.add_argument("url")
    at.add_argument("--description", default="")
    at.set_defaults(func=cmd_attach)
    e = sub.add_parser("extract")
    e.add_argument("slug")
    e.set_defaults(func=cmd_extract)
    m = sub.add_parser("mark")
    m.add_argument("slug")
    m.add_argument("status", choices=["unavailable", "transcribed"])
    m.add_argument("--reason", default="")
    m.add_argument("--method", help="transcribed の場合: 例 'Claude で PDF 画像から手作業で文字起こし'")
    m.set_defaults(func=cmd_mark)
    o = sub.add_parser("ocr", help="スキャン画像PDFを OCR する（slug 省略で needs_ocr 全件）。要 uv sync --extra ocr")
    o.add_argument("slug", nargs="?")
    o.set_defaults(func=cmd_ocr)
    s = sub.add_parser("search")
    s.add_argument("terms", nargs="+", help="すべて含む行を探す（大文字小文字は無視）")
    s.add_argument("-C", "--context", type=int, default=0)
    s.add_argument("--topic")
    s.set_defaults(func=cmd_search)
    st = sub.add_parser("status")
    st.add_argument("-v", "--verbose", action="store_true")
    st.set_defaults(func=cmd_status)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
