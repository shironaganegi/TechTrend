"""コンテンツジェネレーター: トレンドデータからAI記事を自動生成するモジュール。"""
from datetime import datetime, timedelta
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
    try:
        content_text = clean_json_text(response_text)
        res_json = json.loads(content_text)
        
        draft = res_json.get("article", "")
        keywords = res_json.get("search_keywords", [name])
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
            keywords = [name]
            x_post = ""
            image_prompt = ""
            note_intro = ""
        else:
            # Fallback 2: Treat raw text as article, but strip JSON-like wrappers if present
            # If it starts with {, mostly likely it's a broken JSON.
            # We try to find the largest text block.
            logger.warning("Regex fallback failed. Using raw text as draft.")
            draft = response_text
            keywords = [name]
            x_post = ""
            image_prompt = ""
            note_intro = ""

            # Minimal cleanup if it looks like JSON
            if draft.strip().startswith("{") and '"article":' in draft:
                 # Try to strip preamble
                 draft = re.sub(r'^[\s\S]*?"article"\s*:\s*"', '', draft)
                 draft = re.sub(r'",\s*"\w+"[\s\S]*$', '', draft)

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
    
    # Escape quotes in metadata
    if x_post: x_post = x_post.replace('"', '\\"').replace("\n", "\\n")
    if note_intro: note_intro = note_intro.replace('"', '\\"').replace("\n", "\\n")
    if image_prompt: image_prompt = image_prompt.replace('"', '\\"').replace("\n", "\\n")

    frontmatter = f"""---
title: "{title}"
emoji: "{random.choice(emojis)}"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: {json.dumps(topics)}
published: {str(is_published).lower()}
x_viral_post: "{x_post}"
note_intro: "{note_intro}"
image_prompt: "{image_prompt}"
---

"""
    return frontmatter

def load_history():
    history_path = os.path.join(config.DATA_DIR, "history.json")
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_history(tool_name, url):
    history_path = os.path.join(config.DATA_DIR, "history.json")
    history = load_history()
    history.append({
        "name": tool_name,
        "url": url,
        "date": datetime.now().isoformat()
    })
    # Keep only last 100 entries
    history = history[-100:]
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def load_trends_data():
    """Loads the latest trends JSON file from the data directory."""
    data_dir = config.DATA_DIR
    if not os.path.exists(data_dir):
        return []
    
    files = sorted([f for f in os.listdir(data_dir) if f.startswith("trends_")], reverse=True)
    if not files:
        return []
        
    latest_file = os.path.join(data_dir, files[0])
    logger.info(f"Loading data from {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def select_best_candidate(data):
    """Selects the best tool to write about, considering history and diversity."""
    history = load_history()
    cooldown_period = timedelta(days=14)
    cutoff_date = datetime.now() - cooldown_period
    
    recent_posted_urls = []
    for h in history:
        try:
            post_date = datetime.fromisoformat(h['date'])
            if post_date > cutoff_date:
                recent_posted_urls.append(h['url'])
        except (ValueError, KeyError):
            continue
            
    candidates = [item for item in data if item.get('daily_stars', 0) > 0 and item.get('url') not in recent_posted_urls]
    
    # Fallback if everything is filtered
    if not candidates:
        logger.info("All trending topics were posted recently. Picking a random one from top trends anyway.")
        candidates = [item for item in data if item.get('daily_stars', 0) > 0]
    
    if not candidates:
        return None

    # Ensure Source Diversity (Pick top 2 from each source)
    candidates_by_source = {}
    for item in candidates:
        src = item.get('source', 'unknown')
        if src not in candidates_by_source:
            candidates_by_source[src] = []
        candidates_by_source[src].append(item)
    
    final_pool = []
    for src, items in candidates_by_source.items():
        sorted_items = sorted(items, key=lambda x: x.get('daily_stars', 0), reverse=True)
        final_pool.extend(sorted_items[:2])
        
    logger.info(f"Candidate Poll Size: {len(final_pool)} (Sources: {list(candidates_by_source.keys())})")
    
    return random.choice(final_pool)

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

if __name__ == "__main__":
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
            article_title = line.replace("# ", "").replace('"', '\\"')
            break
            
    # generate_article() は本文末尾に隠しブロック(X投稿/note導入/画像プロンプト)を
    # 付加して返すため、ここで抽出してfrontmatterへ移し、本文からは取り除く。
    x_post_match = re.search(r'---X_POST_START---([\s\S]*?)---X_POST_END---', body_content)
    x_viral_post = x_post_match.group(1).strip() if x_post_match else ""
    
    note_intro_match = re.search(r'---NOTE_INTRO_START---([\s\S]*?)---NOTE_INTRO_END---', body_content)
    note_intro = note_intro_match.group(1).strip() if note_intro_match else ""
    
    image_prompt_match = re.search(r'---IMAGE_PROMPT_START---([\s\S]*?)---IMAGE_PROMPT_END---', body_content)
    image_prompt = image_prompt_match.group(1).strip() if image_prompt_match else ""
    
    # Clean body from blocks
    body_content = re.sub(r'---X_POST_START---[\s\S]*?---X_POST_END---\n?', '', body_content)
    body_content = re.sub(r'---NOTE_INTRO_START---[\s\S]*?---NOTE_INTRO_END---\n?', '', body_content)
    body_content = re.sub(r'---IMAGE_PROMPT_START---[\s\S]*?---IMAGE_PROMPT_END---\n?', '', body_content)

    frontmatter = generate_zenn_frontmatter(article_title, top_tool['name'], top_tool.get('source'), x_viral_post, note_intro, image_prompt)
    final_content = frontmatter + body_content
    
    # 5. Save Japanese Article
    filepath_ja = save_article_file(final_content, top_tool)
    
    # 6. Generate & Save English Version
    body_only = body_content
    logger.info("Translating article to English...")
    
    en_body = translate_article_to_english(body_only)
    if en_body:
        en_content = f"""---
title: "{article_title} (English)"
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
