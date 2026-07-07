import importlib.util
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_curate_module():
    path = os.path.join(REPO_ROOT, "scripts", "curate_articles.py")
    spec = importlib.util.spec_from_file_location("curate_articles_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_score_article_fail_marker():
    mod = _load_curate_module()
    fm = 'title = "Sample"'
    body = "記事生成に失敗しました（エラーまたはタイムアウト）。"
    score, reasons = mod.score_article(fm, body)
    assert score == -1000.0
    assert any(r.startswith("FAIL:") for r in reasons)


def test_score_article_thin_penalty():
    mod = _load_curate_module()
    fm = 'title = "Sample"'
    body = "短い本文です。" * 10  # 1200文字未満
    score, reasons = mod.score_article(fm, body)
    assert 'THIN' in reasons


def test_score_article_table_faq_tags_bonus():
    mod = _load_curate_module()
    fm = 'title = "Sample"\ntags = ["AI", "Tools", "Python", "RAG", "LLM", "OSS"]'
    body = (
        "本文の導入段落です。" * 50 + "\n\n"
        "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
        "## FAQ\nよくある質問への回答です。\n\n"
        "## 比較\n他ツールとの比較を行います。\n\n"
        "## 見出し3\nテキスト\n\n"
        "## 見出し4\nテキスト\n"
    )
    score, reasons = mod.score_article(fm, body)
    assert 'table' in reasons
    assert 'faq' in reasons
    assert any(r.startswith('tags=') for r in reasons)


def test_score_article_offtopic_penalty():
    mod = _load_curate_module()
    fm = 'title = "カフェ巡りツール"'
    body = "本文" * 5
    score, reasons = mod.score_article(fm, body)
    assert 'offtopic' in reasons


def test_tool_key_duplicate_extraction():
    mod = _load_curate_module()
    assert mod.tool_key('AIツール「MarkItDown」の紹介') == 'markitdown'
    assert mod.tool_key('タイトルに鉤括弧なし') is None
