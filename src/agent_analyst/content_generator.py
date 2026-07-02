"""コンテンツジェネレーター: トレンドデータからAI記事を自動生成するモジュール。"""
import warnings
import os
import json
import re
import random
import string
import logging
from typing import List, Dict, Any, Optional

from src.agent_analyst.failure_miner import mine_failures
from src.agent_analyst.editor import refine_article
from src.agent_analyst.llm import llm_client
from src.shared.config import config
from src.shared.utils import setup_logging, safe_requests_get
from src.shared.frontmatter import json_escape
from src.shared.article_text import extract_hidden_block, strip_hidden_blocks

# 後方互換 re-export（分割前の import 経路を維持する）
from src.agent_analyst.llm_json import clean_json_text, parse_generation_response
from src.agent_analyst.candidate_selector import (
    select_best_candidate,
    load_history,
    save_to_history,
    load_trends_data,
)

warnings.filterwarnings("ignore", category=FutureWarning)

logger = setup_logging(__name__)

def get_readme_content(github_url):
    """
    Fetches the README content from a GitHub repository to give context to the LLM.
    """
    try:
        # GitHubリポジトリのURLでなければREADME取得を試みない
        # (HackerNews/Qiita/Zenn等のURLで誤ったraw URLを叩き404になるのを防ぐ)
        if "github.com/" not in github_url:
            return "No detailed documentation found."

        parts = github_url.split("github.com/")[1].strip("/").split("/")
        if len(parts) >= 2:
            user = parts[0]
            repo = parts[1]
            for branch in ("main", "master"):
                raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md"
                response = safe_requests_get(raw_url)
                if response and response.status_code == 200:
                    logger.info(f"Retrieved README from {raw_url}")
                    return response.text[:10000]  # Limit context size

    except Exception as e:
        logger.error(f"Failed to fetch README: {e}")

    return "No detailed documentation found."

def generate_article(tool_data: Dict[str, Any], x_hot_words: Optional[List[str]] = None) -> str:
    """
    Gemini を使ってブログ記事ドラフトとバイラルXポストを生成する。
    """
    if x_hot_words is None:
        x_hot_words = []

    name = tool_data.get('name')
    description = tool_data.get('description')
    url = tool_data.get('url')

    logger.info(f"分析中: {name}")
    readme_text = get_readme_content(url)
    failure_context = mine_failures(name)
    x_context = ", ".join(x_hot_words[:10])

    from src.agent_analyst.brain_connector import brain_connector
    strategic_context = brain_connector.get_strategic_context()
    adsense_sop = brain_connector.get_adsense_sop()

    # 1. プロンプトの読み込み
    prompt_template = llm_client.load_prompt("article_generation.txt")
    if not prompt_template:
        return f"# {name}\n\nMetrics error: Prompt file missing."

    prompt = prompt_template.format(
        name=name,
        url=url,
        description=description,
        readme_text=readme_text[:5000],
        failure_context=failure_context,
        x_context=x_context,
        strategic_context=strategic_context[:3000], # Limit to avoid context overflow
        adsense_sop=adsense_sop[:2000]
    )


    if not config.GEMINI_API_KEY:
        return f"# {name}\n\nMock content."

    # 2. Call Gemini
    # Force JSON mode to prevent preamble text
    generation_config = {"response_mime_type": "application/json"}

    response_text = ""
    # Retry loop for JSON generation (Content Quality)
    for attempt in range(2):
        response_text = llm_client.generate_content(prompt, generation_config=generation_config)

        if not response_text:
            continue

        # Quick validation
        if "{" in response_text and "}" in response_text:
            break
        logger.warning(f"Generated content does not look like JSON (Attempt {attempt+1}). Retrying...")

    if not response_text:
        return f"# {name}\n\n記事生成に失敗しました（エラーまたはタイムアウト）。ログを確認してください。"

    # 3. Parse JSON & Extract Content
    parsed = parse_generation_response(response_text, name)
    draft = parsed["article"]
    x_post = parsed["x_post"]
    image_prompt = parsed["image_prompt"]
    note_intro = parsed["note_intro"]

    # 4. アフィリエイト機能は廃止。残存するプレースホルダーのみ除去する。
    final_article = draft.replace("{{RECOMMENDED_PRODUCTS}}", "").replace("{RECOMMENDED_PRODUCTS}", "")

    # 5. Refine with Editor Personality
    try:
        refined_article = refine_article(final_article)
    except Exception as e:
        logger.warning(f"エディターリファインに失敗: {e}")
        refined_article = final_article

    # 6. Append Ad, X Post & Note Intro
    refined_article = append_footer_content(refined_article, x_post, note_intro, image_prompt)

    return refined_article

def translate_article_to_english(content):
    """
    Translates the Japanese Markdown content to English using Gemini.
    """
    # Pre-processing: Remove Zenn-specific blocks (PR notices etc)
    content = re.sub(r':::message[\s\S]*?:::\n?', '', content)

    prompt = f"""
    You are a professional Tech Translator.
    Translate the following Japanese Markdown blog post into high-quality English.

    Requirements:
    - Keep the Markdown format exactly as is (headings, links, code blocks).
    - Maintain the professional and insightful tone.
    - Translate "Recommended Products" section naturally (or keep affiliate links if they are universal, otherwise keep them).
    - Do NOT translate the Frontmatter (YAML block at the top), I will handle it programmatically, BUT if you see it, just leave it or ignore it.
    - Output ONLY the translated markdown content.

    Original Content:
    {content}
    """

    return llm_client.generate_content(prompt)

def append_footer_content(article, x_post, note_intro="", image_prompt=""):
    # Add Hidden X Post
    if x_post:
        article += f"\n\n---X_POST_START---\n{x_post}\n---X_POST_END---\n"

    # Add Hidden Note Intro
    if note_intro:
        article += f"\n\n---NOTE_INTRO_START---\n{note_intro}\n---NOTE_INTRO_END---\n"

    # Add Hidden Image Prompt
    if image_prompt:
        article += f"\n\n---IMAGE_PROMPT_START---\n{image_prompt}\n---IMAGE_PROMPT_END---\n"

    return article

def generate_zenn_frontmatter(title, tool_name, source, x_post="", note_intro="", image_prompt=""):
    """
    Generates Zenn compatible YAML frontmatter.
    """
    emojis = ["🤖", "🚀", "🛠️", "💻", "💡", "🔥", "📈", "🔍"]
    topics = ["AI", "OpenSource", "Tech", "Programming"]
    if source == "github": topics.append("GitHub")
    if "python" in tool_name.lower(): topics.append("Python")

    is_published = config.ZENN_AUTO_PUBLISH

    # YAML値は json_escape でエスケープする（" や改行を安全に埋め込む）。
    # json_escape は前後の " も付与するため、テンプレート側では裸で展開する。
    title_y = json_escape(title)
    x_post_y = json_escape(x_post or "")
    note_intro_y = json_escape(note_intro or "")
    image_prompt_y = json_escape(image_prompt or "")

    frontmatter = f"""---
title: {title_y}
emoji: "{random.choice(emojis)}"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: {json.dumps(topics)}
published: {str(is_published).lower()}
x_viral_post: {x_post_y}
note_intro: {note_intro_y}
image_prompt: {image_prompt_y}
---

"""
    return frontmatter

def save_article_file(content, tool_data):
    """Saves the article to the articles directory with a Zenn-compatible filename."""

    # Generate random 14-char slug
    slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=14))

    os.makedirs(config.ARTICLES_DIR, exist_ok=True)
    file_path = os.path.join(config.ARTICLES_DIR, f"{slug}.md")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Log to history
    save_to_history(tool_data['name'], tool_data['url'])

    logger.info(f"Zenn article saved to: {file_path}")
    logger.info("-" * 30)
    return file_path

def main():
    # 1. Load Data
    trends_data = load_trends_data()
    if not trends_data:
        logger.warning("No trend data found. Run watcher first.")
        exit()

    # Handle new dict format or old list format
    if isinstance(trends_data, dict):
        topics = trends_data.get("topics", [])
        x_hot_words = trends_data.get("x_hot_words", [])
    else:
        topics = trends_data
        x_hot_words = []

    # 2. Select Tool
    top_tool = select_best_candidate(topics)
    if not top_tool:
        logger.warning("No suitable candidates found.")
        exit()

    logger.info(f"Selected Tool: {top_tool['name']} (Source: {top_tool.get('source')})")

    # 3. Generate Content
    body_content = generate_article(top_tool, x_hot_words=x_hot_words)

    if "記事生成に失敗しました" in body_content or "Mock content" in body_content:
        logger.error("Article generation failed. Aborting save.")
        exit(1)

    # 4. Extract Title & Frontmatter
    article_title = "New AI Tool: " + top_tool['name']
    for line in body_content.split("\n"):
        if line.startswith("# "):
            # 生のタイトルを保持する。frontmatter への埋め込み時に json.dumps で
            # 適切にエスケープするため、ここでは手動エスケープしない。
            article_title = line.replace("# ", "").strip()
            break

    # generate_article() は本文末尾に隠しブロック(X投稿/note導入/画像プロンプト)を
    # 付加して返すため、ここで抽出してfrontmatterへ移し、本文からは取り除く。
    x_viral_post = extract_hidden_block(body_content, "x_post")
    note_intro = extract_hidden_block(body_content, "note_intro")
    image_prompt = extract_hidden_block(body_content, "image_prompt")

    # Clean body from blocks
    body_content = strip_hidden_blocks(body_content, ("x_post", "note_intro", "image_prompt"))

    frontmatter = generate_zenn_frontmatter(article_title, top_tool['name'], top_tool.get('source'), x_viral_post, note_intro, image_prompt)
    final_content = frontmatter + body_content

    # 5. Save Japanese Article
    filepath_ja = save_article_file(final_content, top_tool)

    # 6. Generate & Save English Version
    body_only = body_content
    logger.info("Translating article to English...")

    en_body = translate_article_to_english(body_only)
    if en_body:
        # 英語版タイトルは翻訳本文の H1（正しい英語タイトル）を採用する。
        # 抽出できない場合のみ日本語タイトルへフォールバック。
        from src.shared.article_text import extract_first_heading
        en_heading = extract_first_heading(en_body)
        en_display_title = en_heading if en_heading else f"{article_title} (English)"
        en_title_y = json.dumps(en_display_title, ensure_ascii=False)
        en_content = f"""---
title: {en_title_y}
emoji: "🤖"
type: "tech"
topics: []
published: false
---

{en_body}
"""
        filename_en = os.path.basename(filepath_ja).replace(".md", ".en.md")
        os.makedirs(config.EN_ARTICLES_DIR, exist_ok=True)
        filepath_en = os.path.join(config.EN_ARTICLES_DIR, filename_en)

        with open(filepath_en, 'w', encoding='utf-8') as f:
            f.write(en_content)
        logger.info(f"English translation saved to: {filepath_en}")

if __name__ == "__main__":
    main()
