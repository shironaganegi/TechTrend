"""frontmatter 関連の共通ユーティリティ。

Zenn YAML 側（content_generator.py / distributor.py が利用）と
Hugo TOML 側（fix_frontmatter.py / curate_articles.py が利用）の
双方をまとめる。挙動は移動元と一字一句同一。
"""
import json
import re


# --- Zenn YAML 側 ---

def json_escape(value):
    """YAML値を json.dumps でエスケープする(" や改行を安全に埋め込む)。"""
    return json.dumps(value, ensure_ascii=False)


def json_unescape(raw: str) -> str:
    """frontmatter の二重引用符値(JSONエスケープ済み)を安全に復元する。

    書き出し側は json.dumps で値を生成するため、json.loads で復号すれば
    \\\\ や \\t を含むケースも完全に元へ戻せる。万一フォーマットが
    異なる場合は最小限の手動アンエスケープにフォールバックする。
    """
    try:
        return json.loads('"' + raw + '"')
    except Exception:
        return raw.replace("\\n", "\n").replace('\\"', '"')


def get_yaml_str(content: str, key: str):
    """YAML frontmatter から key の文字列値を取り出す。無ければ None。"""
    m = re.search(rf'^{re.escape(key)}:\s*"(.*)"', content, re.MULTILINE)
    return json_unescape(m.group(1)) if m else None


def strip_yaml_frontmatter(content: str) -> str:
    """YAML frontmatter(--- ... ---)を除去した本文を返す。"""
    return re.sub(r'^---[\s\S]*?---\n', '', content)


# --- Hugo TOML 側 ---

_FM_RE = re.compile(r'^\+\+\+\n([\s\S]*?)\n\+\+\+\n?')


def split_toml_frontmatter(content: str):
    """(frontmatter文字列, 本文) を返す。frontmatter が無ければ (None, content)。"""
    m = _FM_RE.match(content)
    if not m:
        return None, content
    return m.group(1), content[m.end():]


def get_toml_value(fm: str, key: str):
    """frontmatter から key の生の値(右辺文字列)を取り出す。無ければ None。"""
    m = re.search(rf'^{re.escape(key)}\s*=\s*(.*)$', fm, re.MULTILINE)
    return m.group(1).strip() if m else None


def set_toml_key(fm: str, key: str, value_literal: str) -> str:
    """frontmatter の key を value_literal(TOML リテラル)へ設定する。

    既存行があれば置換、無ければ末尾に追記。置換は関数置換を用い、
    値に含まれるバックスラッシュ(json.dumps 由来の \\" 等)が
    re の置換仕様で壊れないようにする。
    """
    line = f"{key} = {value_literal}"
    pattern = re.compile(rf'^{re.escape(key)}\s*=.*$', re.MULTILINE)
    if pattern.search(fm):
        return pattern.sub(lambda _m: line, fm, count=1)
    if fm and not fm.endswith('\n'):
        fm += '\n'
    return fm + line
