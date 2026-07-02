"""記事を機械採点し、厳選削減（scaled content 対策）を行う。

AdSense「有用性の低いコンテンツ」是正の一環。全自動で量産された記事群のうち、
薄い/生成失敗/重複の記事をサイト（website/content/posts）から除外し、
良質な上位のみを残す。

採点対象は日本語記事（*.md）。英語版（*.en.md）は対の日本語記事の keep/drop に追従する。

除外は削除ではなく trash_posts/ への移動（可逆・git 履歴保持）。

使い方:
    python scripts/curate_articles.py                      # 採点してランキング/分布を表示（何も移動しない）
    python scripts/curate_articles.py --keep 100           # keep=100 の場合の keep/drop 件数を表示
    python scripts/curate_articles.py --keep 100 --prune --apply   # 実際に drop を trash_posts へ移動
"""
import os
import re
import sys
import csv
import argparse
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from src.shared.frontmatter import (  # noqa: E402
    split_toml_frontmatter as split_frontmatter,
    get_toml_value,
)

POSTS_DIR = os.path.join(REPO_ROOT, "website", "content", "posts")
TRASH_DIR = os.path.join(REPO_ROOT, "trash_posts")

_CODE_FENCE_RE = re.compile(r'```[\s\S]*?```')
_HTML_TAG_RE = re.compile(r'<[^>]+>')

FAIL_MARKERS = ('記事生成に失敗しました', 'Mock content', 'Metrics error', '"article":')
OFF_TOPIC_KEYWORDS = ('カフェ', 'ノマド', 'グルメ', '占い', '恋愛', 'ダイエット')


def plain_text(body):
    """コード/HTML/表を除いたプレーン本文を返す（文字数計測用）。"""
    text = _CODE_FENCE_RE.sub('', body)
    text = _HTML_TAG_RE.sub('', text)
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith('|') or re.fullmatch(r'[-*_]{3,}', line):
            continue
        lines.append(line)
    return ' '.join(lines)


def tool_key(title):
    """タイトル内の最初の「...」をツール識別子として返す（重複検出用）。"""
    m = re.search(r'「([^」]+)」', title)
    return m.group(1).strip().lower() if m else None


def score_article(fm, body):
    """(score, reasons) を返す。score が高いほど良質。"""
    reasons = []

    # 生成失敗・JSON漏れは即 drop
    for mk in FAIL_MARKERS:
        if mk in body:
            return -1000.0, [f"FAIL:{mk}"]

    text = plain_text(body)
    n = len(text)

    score = 0.0
    # 本文量（2500文字で満点40）
    length_pts = min(n, 2500) / 2500 * 40
    score += length_pts
    reasons.append(f"len={n}({length_pts:.0f})")

    has_table = bool(re.search(r'^\|.*\|', body, re.MULTILINE))
    has_faq = ('FAQ' in body) or ('よくある質問' in body)
    has_expert = 'expert-opinion' in body
    has_cmp = ('比較' in body) or has_table

    if has_table:
        score += 12; reasons.append('table')
    if has_faq:
        score += 12; reasons.append('faq')
    if has_expert:
        score += 8; reasons.append('expert')
    if has_cmp:
        score += 6; reasons.append('cmp')

    # タグの具体性（AI/Tools 以外の具体タグ数）
    tags_raw = get_toml_value(fm, 'tags') or '[]'
    specific = 0
    for t in re.findall(r'"([^"]+)"', tags_raw):
        if t not in ('AI', 'Tools'):
            specific += 1
    tag_pts = min(specific, 4) * 4
    score += tag_pts
    reasons.append(f"tags={specific}({tag_pts})")

    # 見出し数（構造の充実）
    h2 = len(re.findall(r'^##\s', body, re.MULTILINE))
    if h2 >= 4:
        score += 6; reasons.append(f'h2={h2}')

    # 極端に短い本文はペナルティ
    if n < 1200:
        score -= 30; reasons.append('THIN')

    # サイト趣旨から外れた話題
    title_raw = get_toml_value(fm, 'title') or ''
    if any(kw in (title_raw + body[:400]) for kw in OFF_TOPIC_KEYWORDS):
        score -= 15; reasons.append('offtopic')

    return score, reasons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keep', type=int, default=None, help='残す記事数（上位N）')
    parser.add_argument('--prune', action='store_true', help='drop を trash_posts へ移動する準備')
    parser.add_argument('--apply', action='store_true', help='実際に移動を実行（--prune と併用）')
    parser.add_argument('--csv', default=os.path.join(REPO_ROOT, 'scripts', 'article_scores.csv'))
    args = parser.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception as e:
        print(f"[WARN] stdout reconfigure failed: {e}", file=sys.stderr)

    ja_files = sorted(f for f in os.listdir(POSTS_DIR) if f.endswith('.md') and not f.endswith('.en.md'))

    rows = []
    for f in ja_files:
        with open(os.path.join(POSTS_DIR, f), 'r', encoding='utf-8') as fh:
            content = fh.read()
        fm, body = split_frontmatter(content)
        if fm is None:
            continue
        score, reasons = score_article(fm, body)
        title = (get_toml_value(fm, 'title') or '').strip('"')
        rows.append({'file': f, 'score': score, 'tool': tool_key(title) or '',
                     'title': title, 'reasons': ' '.join(reasons)})

    # 重複ツールのペナルティ（同一ツールは最高スコア1本を残し他を減点）
    by_tool = {}
    for r in rows:
        if r['tool']:
            by_tool.setdefault(r['tool'], []).append(r)
    for tool, group in by_tool.items():
        if len(group) > 1:
            group.sort(key=lambda x: x['score'], reverse=True)
            for dup in group[1:]:
                dup['score'] -= 50
                dup['reasons'] += ' DUP'

    rows.sort(key=lambda x: x['score'], reverse=True)

    with open(args.csv, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['rank', 'file', 'score', 'tool', 'title', 'reasons'])
        w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow({'rank': i, **r, 'score': f"{r['score']:.1f}"})

    # スコア分布
    print("================ スコア分布 ================")
    buckets = [(-10**9, 0), (0, 20), (20, 40), (40, 60), (60, 80), (80, 10**9)]
    labels = ['<0(要drop)', '0-20', '20-40', '40-60', '60-80', '80+']
    for (lo, hi), lab in zip(buckets, labels):
        c = sum(1 for r in rows if lo <= r['score'] < hi)
        print(f"  {lab:>10}: {c}")
    print(f"総日本語記事: {len(rows)}  / CSV: {os.path.relpath(args.csv, REPO_ROOT)}")

    if args.keep is None:
        print("\n→ --keep N を指定すると keep/drop の内訳を表示します。")
        return

    keep_rows = rows[:args.keep]
    drop_rows = rows[args.keep:]
    print(f"\n================ keep={args.keep} ================")
    print(f"KEEP: {len(keep_rows)}  DROP: {len(drop_rows)}")
    print(f"KEEP 最低スコア: {keep_rows[-1]['score']:.1f} / DROP 最高スコア: {drop_rows[0]['score']:.1f}" if drop_rows else "全件 keep")
    print("\n-- DROP 上位10（惜しくも外れた記事）--")
    for r in drop_rows[:10]:
        print(f"  {r['score']:.1f}  {r['title'][:50]}")
    print("\n-- DROP 下位10（明確に弱い記事）--")
    for r in drop_rows[-10:]:
        print(f"  {r['score']:.1f}  [{r['reasons']}]  {r['title'][:40]}")

    if not args.prune:
        print("\n→ 移動するには --prune --apply を付けてください。")
        return

    # 移動対象（drop の JA と対応する EN）
    os.makedirs(TRASH_DIR, exist_ok=True)
    moved = 0
    for r in drop_rows:
        ja = r['file']
        en = ja[:-3] + '.en.md'
        for name in (ja, en):
            src = os.path.join(POSTS_DIR, name)
            if os.path.exists(src):
                if args.apply:
                    shutil.move(src, os.path.join(TRASH_DIR, name))
                moved += 1
    print(f"\n{'移動実行' if args.apply else 'ドライラン'}: {moved} ファイル（JA+EN） → trash_posts/")
    if not args.apply:
        print("→ 実際に移動するには --apply を付けてください。")


if __name__ == "__main__":
    main()
