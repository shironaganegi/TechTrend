"""記事本文からメタ情報（description / タイトル）を抽出する共通ロジック。

hugo.py（新規記事生成）と scripts/（既存記事の一括是正）の双方から利用し、
description 生成ロジックの唯一の source of truth とする。

背景: 従来は description が全記事テンプレ（`AIツール「{title}」の活用法を紹介`）で、
重複コンテンツシグナルとなっていた。本文の最初の実段落から固有の description を
生成することでこれを解消する。
"""
import re

# 本文末尾に付く隠しブロック（X投稿 / note導入 / 画像プロンプト）
_HIDDEN_BLOCK_RE = re.compile(
    r'---(?:X_POST|NOTE_INTRO|IMAGE_PROMPT)_START---[\s\S]*?'
    r'---(?:X_POST|NOTE_INTRO|IMAGE_PROMPT)_END---\n?'
)
# フェンス付きコードブロック
_CODE_FENCE_RE = re.compile(r'```[\s\S]*?```')
# 残存 HTML タグ
_HTML_TAG_RE = re.compile(r'<[^>]+>')

# 本文末尾に付く隠しブロックの種類ごとの (開始マーカー, 終了マーカー)
HIDDEN_BLOCKS = {
    "x_post": ("---X_POST_START---", "---X_POST_END---"),
    "note_intro": ("---NOTE_INTRO_START---", "---NOTE_INTRO_END---"),
    "image_prompt": ("---IMAGE_PROMPT_START---", "---IMAGE_PROMPT_END---"),
}


def extract_hidden_block(text: str, kind: str) -> str:
    """text から kind に対応する隠しブロックの中身を抽出する。無ければ空文字。"""
    start, end = HIDDEN_BLOCKS[kind]
    m = re.search(rf'{re.escape(start)}([\s\S]*?){re.escape(end)}', text)
    return m.group(1).strip() if m else ""


def strip_hidden_blocks(text: str, kinds) -> str:
    """text から kinds で指定した種類の隠しブロックを除去する。"""
    for kind in kinds:
        start, end = HIDDEN_BLOCKS[kind]
        text = re.sub(rf'{re.escape(start)}[\s\S]*?{re.escape(end)}\n?', '', text)
    return text


def extract_first_heading(body: str) -> str:
    """本文中の最初の Markdown H1（`# ...`）テキストを返す。無ければ空文字。"""
    for line in body.splitlines():
        s = line.strip()
        if s.startswith('# '):
            return s[2:].strip()
    return ""


def build_description(body: str, max_len: int = 120) -> str:
    """本文の最初の「実段落」から description を生成する。

    見出し・コードブロック・HTML ブロック・表・水平線・引用・箇条書きを除外し、
    最初の意味のある散文段落を句読点境界で ``max_len`` 程度に整形して返す。
    抽出できなければ空文字を返す（呼び出し側でフォールバックする想定）。
    """
    text = _HIDDEN_BLOCK_RE.sub('', body)
    text = _CODE_FENCE_RE.sub('', text)

    paragraph_lines = []
    started = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if started:
                break  # 実段落が一度始まったら空行で終了
            continue
        if line.startswith('#'):                      # 見出し
            continue
        if line.startswith('|'):                      # 表
            continue
        if line.startswith('>'):                      # 引用
            continue
        if re.fullmatch(r'[-*_]{3,}', line):          # 水平線
            continue
        if re.match(r'[-*+]\s', line):                # 箇条書き
            continue
        if line.startswith('<'):                      # HTML ブロック（expert-opinion 等）
            continue
        started = True
        paragraph_lines.append(line)

    paragraph = ' '.join(paragraph_lines)

    # インライン Markdown / HTML をプレーン化
    paragraph = _HTML_TAG_RE.sub('', paragraph)
    paragraph = re.sub(r'`([^`]*)`', r'\1', paragraph)               # inline code
    paragraph = re.sub(r'\*\*([^*]+)\*\*', r'\1', paragraph)         # bold
    paragraph = re.sub(r'\*([^*]+)\*', r'\1', paragraph)             # italic
    paragraph = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', paragraph)   # links
    paragraph = re.sub(r'\s+', ' ', paragraph).strip()

    if not paragraph:
        return ""
    return _truncate(paragraph, max_len)


def _truncate(text: str, max_len: int) -> str:
    """句読点境界を優先して text を max_len 程度に切り詰める。"""
    if len(text) <= max_len:
        return text
    window = text[:max_len]
    cut = max(
        window.rfind('。'),
        window.rfind('！'),
        window.rfind('？'),
        window.rfind('. '),
    )
    if cut >= max_len * 0.5:
        # '. ' の場合は '.' まで含める
        end = cut + 1
        return window[:end].strip()
    # 文末境界が無ければ単語（空白）境界で切る（英語で語の途中切れを避ける）
    sp = window.rfind(' ')
    if sp >= max_len * 0.5:
        return window[:sp].rstrip() + '…'
    return window.rstrip() + '…'
