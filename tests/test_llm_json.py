from src.agent_analyst.llm_json import parse_generation_response


def test_parse_generation_response_normal_json():
    response_text = (
        '{"article": "# Title\\n\\nBody text", '
        '"search_keywords": ["kw1", "kw2"], '
        '"x_viral_post": "post!", '
        '"image_prompt": "an image", '
        '"note_intro": "intro text"}'
    )
    result = parse_generation_response(response_text, "default-tool")
    assert result["article"] == "# Title\n\nBody text"
    assert result["keywords"] == ["kw1", "kw2"]
    assert result["x_post"] == "post!"
    assert result["image_prompt"] == "an image"
    assert result["note_intro"] == "intro text"


def test_parse_generation_response_regex_recovery():
    # 不正な JSON だが "article": "..." パターンにはマッチする文字列
    response_text = '{"article": "recovered content with \\\\n newline", "other_field"' + '}'
    result = parse_generation_response(response_text, "default-tool")
    assert "recovered content" in result["article"]
    assert result["keywords"] == ["default-tool"]
    assert result["x_post"] == ""


def test_parse_generation_response_raw_text_fallback():
    response_text = "This is not JSON at all, just plain broken text {"
    result = parse_generation_response(response_text, "default-tool")
    assert result["article"] == response_text
    assert result["keywords"] == ["default-tool"]
    assert result["x_post"] == ""
    assert result["image_prompt"] == ""
    assert result["note_intro"] == ""
