import os
import json
import re
from datetime import datetime
from src.shared.config import config
from src.shared.utils import setup_logging
from src.shared.tagging import derive_tags
from src.shared.article_text import build_description, extract_first_heading, strip_hidden_blocks
from src.shared.branding import SITE_BASE_URL, SITE_AUTHOR

logger = setup_logging(__name__)

class HugoPublisher:
    def save_article(self, title, body, zenn_url, original_filename, lang="ja", ogp_url=None):
        os.makedirs(config.WEBSITE_CONTENT_DIR, exist_ok=True)

        date_str = datetime.now().isoformat()
        target_filename = os.path.basename(original_filename)
        slug = re.sub(r'\.(en\.)?md$', '', target_filename)

        # 英語記事は frontmatter title が「日本語タイトル (English)」で渡ってくるため、
        # 本文の H1（正しい英語タイトル）を優先採用する。
        if lang == "en":
            en_heading = extract_first_heading(body)
            if en_heading:
                title = en_heading

        # 内容に応じた具体的なトピックタグを導出（検索・回遊性向上）
        tags = derive_tags(title, body)

        # description は本文の最初の実段落から生成（テンプレ文言を廃止し重複を解消）。
        # 抽出できない場合のみタイトルベースのフォールバックを使う。
        desc_max = 160 if lang == "en" else 110
        description = build_description(body, max_len=desc_max)
        if not description:
            description = title

        # canonicalUrl は各ページ自身の URL を指す（英語→日本語の相互 canonical を撤廃）。
        if lang == "en":
            canonical_url = f"{SITE_BASE_URL}/en/posts/{slug}/"
        else:
            canonical_url = f"{SITE_BASE_URL}/posts/{slug}/"

        cover_yaml = ""
        # Disabled OGP logic placeholder

        # TOML値は json.dumps でエスケープする（" を含むタイトルでも壊れないように）。
        # JSON文字列のエスケープ仕様は TOML basic string と互換。
        title_toml = json.dumps(title, ensure_ascii=False)
        description_toml = json.dumps(description, ensure_ascii=False)
        author_toml = json.dumps(SITE_AUTHOR, ensure_ascii=False)

        frontmatter = f"""+++
title = {title_toml}
date = "{date_str}"
tags = {json.dumps(tags)}
draft = false
description = {description_toml}
author = {author_toml}
canonicalUrl = "{canonical_url}"{cover_yaml}
+++

"""
        # Clean body for Hugo
        hugo_body = body.replace("<!-- AFFILIATE_START -->", "").replace("<!-- AFFILIATE_END -->", "")
        hugo_body = strip_hidden_blocks(hugo_body, ("x_post", "note_intro"))

        # Convert Zenn syntax (:::message) to blockquotes
        def message_to_quote(match):
            content = match.group(1)
            # Prefix each line with >
            quoted = "\n".join([f"> {line}" for line in content.strip().split("\n")])
            return f"\n{quoted}\n"
            
        hugo_body = re.sub(r':::message\n([\s\S]*?)\n:::', message_to_quote, hugo_body)
        
        if lang == "ja":
            # No footer needed for main site (or maybe affiliate disclaimer if wanted)
            footer = "" 
        else:
            footer = f"\n\n---\n\n> This article is also available in [Japanese]({zenn_url}).\n" # Actually zenn_url is now website_url so this links to JA version on same site

        
        output_path = os.path.join(config.WEBSITE_CONTENT_DIR, target_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + hugo_body + footer)
        
        logger.info(f"Saved Hugo article ({lang}) to: {output_path}")
