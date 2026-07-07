import importlib.util
import os
import re
import json

from src.agent_analyst.content_generator import generate_zenn_frontmatter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _unquote(raw: str) -> str:
    """distributor._unquote と同じロジック(ラウンドトリップ検証用にコピー)。"""
    try:
        return json.loads('"' + raw + '"')
    except Exception:
        return raw.replace("\\n", "\n").replace('\\"', '"')


def _parse_title(content: str) -> str:
    """distributor.parse_article のタイトル抽出相当。"""
    title_match = re.search(r'^title:\s*"(.*)"', content, re.MULTILINE)
    return _unquote(title_match.group(1)) if title_match else "No Title"


def test_frontmatter_title_roundtrip_quote():
    title = 'Tool "Awesome" Release'
    fm = generate_zenn_frontmatter(title, "tool", "github")
    assert _parse_title(fm) == title


def test_frontmatter_title_roundtrip_newline():
    title = "Line1\nLine2"
    fm = generate_zenn_frontmatter(title, "tool", "github")
    assert _parse_title(fm) == title


def test_frontmatter_title_roundtrip_backslash():
    title = r"C:\path\to\tool and \"quoted\" text"
    fm = generate_zenn_frontmatter(title, "tool", "github")
    assert _parse_title(fm) == title


def _load_fix_frontmatter_module():
    path = os.path.join(REPO_ROOT, "scripts", "fix_frontmatter.py")
    spec = importlib.util.spec_from_file_location("fix_frontmatter_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_split_toml_frontmatter():
    mod = _load_fix_frontmatter_module()
    content = '+++\ntitle = "Hello"\n+++\n\nBody text\n'
    fm, body = mod.split_frontmatter(content)
    assert fm == 'title = "Hello"'
    assert body == '\nBody text\n'


def test_get_toml_value():
    mod = _load_fix_frontmatter_module()
    fm = 'title = "Hello"\nauthor = "someone"'
    assert mod.get_toml_value(fm, 'title') == '"Hello"'
    assert mod.get_toml_value(fm, 'missing') is None


def test_set_toml_key_replace_existing():
    mod = _load_fix_frontmatter_module()
    fm = 'title = "Hello"\nauthor = "someone"'
    new_fm = mod.set_toml_key(fm, 'title', '"World"')
    assert mod.get_toml_value(new_fm, 'title') == '"World"'
    assert mod.get_toml_value(new_fm, 'author') == '"someone"'


def test_set_toml_key_append_new():
    mod = _load_fix_frontmatter_module()
    fm = 'title = "Hello"'
    new_fm = mod.set_toml_key(fm, 'author', '"someone"')
    assert mod.get_toml_value(new_fm, 'author') == '"someone"'


def test_set_toml_key_with_backslash_value():
    """値にバックスラッシュを含む置換が re.sub の後方参照解釈で壊れないことを確認。"""
    mod = _load_fix_frontmatter_module()
    fm = 'description = "old value"'
    # json.dumps 由来のバックスラッシュを含むリテラル(例: \\ や \")
    backslash_value = json.dumps('C:\\Users\\test "quoted"', ensure_ascii=False)
    new_fm = mod.set_toml_key(fm, 'description', backslash_value)
    assert mod.get_toml_value(new_fm, 'description') == backslash_value
    assert json.loads(mod.get_toml_value(new_fm, 'description')) == 'C:\\Users\\test "quoted"'
