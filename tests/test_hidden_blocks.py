import re

# content_generator.py __main__ ブロック(394-406行)の正規表現をそのまま使用する。


def _extract(body_content, start, end):
    m = re.search(rf'{start}([\s\S]*?){end}', body_content)
    return m.group(1).strip() if m else ""


def _strip(body_content, start, end):
    return re.sub(rf'{start}[\s\S]*?{end}\n?', '', body_content)


def test_extract_x_post_block():
    content = "本文\n\n---X_POST_START---\nXの投稿文\n---X_POST_END---\n"
    assert _extract(content, '---X_POST_START---', '---X_POST_END---') == "Xの投稿文"


def test_extract_note_intro_block():
    content = "本文\n\n---NOTE_INTRO_START---\nnote導入文\n---NOTE_INTRO_END---\n"
    assert _extract(content, '---NOTE_INTRO_START---', '---NOTE_INTRO_END---') == "note導入文"


def test_extract_image_prompt_block():
    content = "本文\n\n---IMAGE_PROMPT_START---\n画像プロンプト\n---IMAGE_PROMPT_END---\n"
    assert _extract(content, '---IMAGE_PROMPT_START---', '---IMAGE_PROMPT_END---') == "画像プロンプト"


def test_extract_missing_block_returns_empty():
    content = "本文だけ"
    assert _extract(content, '---X_POST_START---', '---X_POST_END---') == ""


def test_strip_all_three_hidden_blocks():
    content = (
        "本文\n"
        "\n\n---X_POST_START---\nXの投稿文\n---X_POST_END---\n"
        "\n\n---NOTE_INTRO_START---\nnote導入文\n---NOTE_INTRO_END---\n"
        "\n\n---IMAGE_PROMPT_START---\n画像プロンプト\n---IMAGE_PROMPT_END---\n"
    )
    stripped = _strip(content, '---X_POST_START---', '---X_POST_END---')
    stripped = _strip(stripped, '---NOTE_INTRO_START---', '---NOTE_INTRO_END---')
    stripped = _strip(stripped, '---IMAGE_PROMPT_START---', '---IMAGE_PROMPT_END---')
    assert stripped == "本文\n\n\n\n\n\n\n"


def test_hugo_strips_only_x_post_and_note_intro():
    """hugo.py は image_prompt を除去しない現行挙動を確認する(揃えない)。"""
    content = (
        "本文\n\n---X_POST_START---\nXの投稿文\n---X_POST_END---\n"
        "\n\n---NOTE_INTRO_START---\nnote導入文\n---NOTE_INTRO_END---\n"
        "\n\n---IMAGE_PROMPT_START---\n画像プロンプト\n---IMAGE_PROMPT_END---\n"
    )
    hugo_body = re.sub(r'---X_POST_START---[\s\S]*?---X_POST_END---\n?', '', content)
    hugo_body = re.sub(r'---NOTE_INTRO_START---[\s\S]*?---NOTE_INTRO_END---\n?', '', hugo_body)
    assert '---IMAGE_PROMPT_START---' in hugo_body
    assert '---X_POST_START---' not in hugo_body
    assert '---NOTE_INTRO_START---' not in hugo_body
