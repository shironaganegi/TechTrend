"""LLM のレスポンステキストから JSON を抽出・パースする共通ロジック。"""
import json
import re
import logging

from src.shared.utils import setup_logging

logger = setup_logging(__name__)


def clean_json_text(text):
    """
    Robustly extracts JSON object from text using regex.
    Handles cases where text has preambles or markdown code blocks.
    """
    text = text.strip()

    # 1. Try to find JSON within code blocks
    code_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
    if code_block_match:
        return code_block_match.group(1)

    # 2. Try to find the first '{' and the last '}'
    # This handles "Here is the JSON: { ... }"
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        return json_match.group(1)

    # 3. Fallback to original cleanup
    return text.strip()


def parse_generation_response(response_text, default_keyword):
    """LLM のレスポンステキストから記事コンテンツを抽出する。

    正常な JSON パースに失敗した場合は Regex フォールバックを2段階で試みる。
    戻り値は dict: article/keywords/x_post/image_prompt/note_intro。
    """
    # 3. Parse JSON & Extract Content
    try:
        content_text = clean_json_text(response_text)
        res_json = json.loads(content_text)

        draft = res_json.get("article", "")
        keywords = res_json.get("search_keywords", [default_keyword])
        x_post = res_json.get("x_viral_post", "")
        image_prompt = res_json.get("image_prompt", "")
        note_intro = res_json.get("note_intro", "")

    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"CRITICAL: JSON Parsing Failed: {e}. Raw text len: {len(response_text)}")

        # Fallback 1: Try to extract "article" using Regex
        # Look for "article": "..." pattern, handling escaped quotes roughly
        article_match = re.search(r'"article"\s*:\s*"(.*?)",\s*"\w+"', response_text, re.DOTALL)
        if article_match:
            draft = article_match.group(1).replace('\\"', '"').replace('\\n', '\n')
            logger.info("Recovered article content using Regex fallback.")
            keywords = [default_keyword]
            x_post = ""
            image_prompt = ""
            note_intro = ""
        else:
            # Fallback 2: Treat raw text as article, but strip JSON-like wrappers if present
            # If it starts with {, mostly likely it's a broken JSON.
            # We try to find the largest text block.
            logger.warning("Regex fallback failed. Using raw text as draft.")
            draft = response_text
            keywords = [default_keyword]
            x_post = ""
            image_prompt = ""
            note_intro = ""

            # Minimal cleanup if it looks like JSON
            if draft.strip().startswith("{") and '"article":' in draft:
                 # Try to strip preamble
                 draft = re.sub(r'^[\s\S]*?"article"\s*:\s*"', '', draft)
                 draft = re.sub(r'",\s*"\w+"[\s\S]*$', '', draft)

    return {
        "article": draft,
        "keywords": keywords,
        "x_post": x_post,
        "image_prompt": image_prompt,
        "note_intro": note_intro,
    }
