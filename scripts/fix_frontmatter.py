"""既存の公開済み記事（website/content/posts/*.md）の frontmatter を一括是正する。

背景（AdSense「有用性の低いコンテンツ」是正）:
- 日本語 description が全記事テンプレ（`AIツール「{title}」の活用法を紹介`）＝重複シグナル。
- 英語 description が壊れている（`Introduction to {日本語タイトル} (English)`）。
- 英語 title が「日本語タイトル (English)」で、<title>/一覧/OGP が日本語。
- 英語 canonicalUrl が日本語版 URL を指し「複製」と宣言している。

本スクリプトは審査官が実際に見る公開記事を現物是正する:
- description を本文の最初の実段落から再生成（build_description）。
- 英語記事は title を本文 H1（正しい英語）に、canonicalUrl を英語自身の URL に。
- 全記事に author を付与。

冪等: 何度実行しても同じ結果になる（description は本文から決定的に再計算）。
既定はドライラン。実際に書き込むには --apply を付ける。

使い方:
    python scripts/fix_frontmatter.py            # ドライラン（差分サンプル表示のみ）
    python scripts/fix_frontmatter.py --apply    # 実際に書き込む
"""
import os
import re
import sys
import json
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from src.shared.article_text import build_description, extract_first_heading  # noqa: E402
from src.shared.branding import SITE_BASE_URL, SITE_AUTHOR  # noqa: E402

POSTS_DIR = os.path.join(REPO_ROOT, "website", "content", "posts")

_FM_RE = re.compile(r'^\+\+\+\n([\s\S]*?)\n\+\+\+\n?')


def split_frontmatter(content: str):
    """(frontmatter文字列, 本文) を返す。frontmatter が無ければ (None, content)。"""
    m = _FM_RE.match(content)
    if not m:
        return None, content
    return m.group(1), content[m.end():]


def get_toml_value(fm: str, key: str):
    """frontmatter から key の生の値（右辺文字列）を取り出す。無ければ None。"""
    m = re.search(rf'^{re.escape(key)}\s*=\s*(.*)$', fm, re.MULTILINE)
    return m.group(1).strip() if m else None


def set_toml_key(fm: str, key: str, value_literal: str) -> str:
    """frontmatter の key を value_literal（TOML リテラル）へ設定する。

    既存行があれば置換、無ければ末尾に追記。置換は関数置換を用い、
    値に含まれるバックスラッシュ（json.dumps 由来の \\" 等）が
    re の置換仕様で壊れないようにする。
    """
    line = f"{key} = {value_literal}"
    pattern = re.compile(rf'^{re.escape(key)}\s*=.*$', re.MULTILINE)
    if pattern.search(fm):
        return pattern.sub(lambda _m: line, fm, count=1)
    if fm and not fm.endswith('\n'):
        fm += '\n'
    return fm + line


def strip_english_suffix(title: str) -> str:
    """タイトル末尾の ' (English)' を除去する。"""
    return re.sub(r'\s*\(English\)\s*$', '', title).strip()


_CJK_RE = re.compile(r'[぀-ヿ一-鿿]')


def is_bad_description(desc: str, is_en: bool) -> bool:
    """既存 description がテンプレ／破損で再生成すべきかを判定する。

    人手で書かれた良質な description（プレミアム記事など）は温存する。
    """
    if not desc:
        return True
    if is_en:
        if desc.startswith('Introduction to'):
            return True
        if desc.rstrip().endswith('(English)'):
            return True
        if _CJK_RE.search(desc):  # 英語 description に日本語混入 = 破損
            return True
        return False
    # 日本語: 旧テンプレ「AIツール「...」の活用法を紹介」のみ再生成対象
    return bool(re.fullmatch(r'AIツール「.*」の活用法を紹介', desc))


def fix_file(path: str):
    """1ファイルを是正した新コンテンツを返す。変更が無ければ None。"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 一部の手作り記事は UTF-8 BOM + CRLF。BOM を除去し改行を LF に正規化してから処理する
    # （これをしないと frontmatter 正規表現が先頭マッチせずスキップされる）。
    content = content.lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')

    fm, body = split_frontmatter(content)
    if fm is None:
        return None  # frontmatter 不在（想定外）はスキップ

    filename = os.path.basename(path)
    is_en = filename.endswith('.en.md')
    slug = re.sub(r'\.(en\.)?md$', '', filename)

    new_fm = fm

    # --- title（英語記事のみ）---
    if is_en:
        heading = extract_first_heading(body)
        if heading:
            new_title = heading
        else:
            # H1 が無い場合は既存タイトルから (English) を除去（次善策）
            raw = get_toml_value(fm, 'title')
            try:
                cur = json.loads(raw) if raw else ''
            except Exception:
                cur = (raw or '').strip('"')
            new_title = strip_english_suffix(cur) or cur
        new_fm = set_toml_key(new_fm, 'title', json.dumps(new_title, ensure_ascii=False))

    # --- description（本文から再生成）---
    # title を決定（英語はH1、日本語は既存title）してフォールバックに使う
    raw_title = get_toml_value(new_fm, 'title')
    try:
        title_text = json.loads(raw_title) if raw_title else slug
    except Exception:
        title_text = (raw_title or slug).strip('"')

    existing_desc_raw = get_toml_value(new_fm, 'description')
    try:
        existing_desc = json.loads(existing_desc_raw) if existing_desc_raw else ''
    except Exception:
        existing_desc = (existing_desc_raw or '').strip('"')

    if is_bad_description(existing_desc, is_en):
        desc_max = 160 if is_en else 110
        description = build_description(body, max_len=desc_max) or title_text
        new_fm = set_toml_key(new_fm, 'description', json.dumps(description, ensure_ascii=False))
    # 良質な既存 description はそのまま温存する

    # --- author ---
    new_fm = set_toml_key(new_fm, 'author', json.dumps(SITE_AUTHOR, ensure_ascii=False))

    # --- canonicalUrl（自ページを指す）---
    if is_en:
        canonical = f"{SITE_BASE_URL}/en/posts/{slug}/"
    else:
        canonical = f"{SITE_BASE_URL}/posts/{slug}/"
    new_fm = set_toml_key(new_fm, 'canonicalUrl', json.dumps(canonical, ensure_ascii=False))

    new_content = f"+++\n{new_fm}\n+++\n\n{body.lstrip(chr(10))}"
    if new_content == content:
        return None
    return new_content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='実際にファイルへ書き込む')
    parser.add_argument('--samples', type=int, default=3, help='表示する差分サンプル数')
    args = parser.parse_args()

    # Windows コンソール(cp932)でも UTF-8 を出力できるようにする（表示のみ・ファイルはUTF-8）
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    if not os.path.isdir(POSTS_DIR):
        print(f"[ERROR] posts ディレクトリが見つかりません: {POSTS_DIR}")
        sys.exit(1)

    files = sorted(f for f in os.listdir(POSTS_DIR) if f.endswith('.md'))
    ja_files = [f for f in files if not f.endswith('.en.md')]
    en_files = [f for f in files if f.endswith('.en.md')]

    changed = 0
    shown = 0
    for f in files:
        path = os.path.join(POSTS_DIR, f)
        new_content = fix_file(path)
        if new_content is None:
            continue
        changed += 1
        if shown < args.samples:
            fm, _ = split_frontmatter(new_content)
            print(f"\n----- {f} -----")
            for key in ('title', 'description', 'author', 'canonicalUrl'):
                print(f"  {key} = {get_toml_value(fm, key)}")
            shown += 1
        if args.apply:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new_content)

    print("\n================ SUMMARY ================")
    print(f"対象ファイル総数 : {len(files)} (JA={len(ja_files)}, EN={len(en_files)})")
    print(f"変更対象         : {changed}")
    print(f"モード           : {'APPLY（書き込み実行）' if args.apply else 'DRY-RUN（未書き込み）'}")
    if not args.apply:
        print("→ 問題なければ --apply を付けて再実行してください。")


if __name__ == "__main__":
    main()
