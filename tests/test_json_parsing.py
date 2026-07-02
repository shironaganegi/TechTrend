from src.agent_analyst.content_generator import clean_json_text


def test_clean_json_text_code_block():
    text = '前置きです\n```json\n{"a": 1, "b": "x"}\n```\n後ろのテキスト'
    assert clean_json_text(text) == '{"a": 1, "b": "x"}'


def test_clean_json_text_with_preamble():
    text = 'Here is the JSON: {"a": 1, "b": "x"}'
    assert clean_json_text(text) == '{"a": 1, "b": "x"}'


def test_clean_json_text_raw_json():
    text = '{"a": 1, "b": "x"}'
    assert clean_json_text(text) == '{"a": 1, "b": "x"}'


def test_clean_json_text_no_json():
    text = 'no json here at all'
    assert clean_json_text(text) == 'no json here at all'
