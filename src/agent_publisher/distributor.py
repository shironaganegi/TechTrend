"""
配信オーケストレーター: 生成された記事をQiita, Zenn, X (Twitter), BlueSky, Discord等に
マルチ配信するモジュール。
"""
import os
import glob
import logging
from typing import Tuple, Optional
from src.shared.config import config
from src.shared.utils import setup_logging
from src.shared.frontmatter import get_yaml_str, strip_yaml_frontmatter

from src.agent_publisher.platforms.qiita import QiitaPublisher
from src.agent_publisher.platforms.bluesky import BlueSkyPublisher
from src.agent_publisher.platforms.twitter import TwitterPublisher
from src.agent_publisher.platforms.hugo import HugoPublisher
from src.agent_publisher.platforms.discord import DiscordPublisher

logger = setup_logging(__name__)


def get_latest_article() -> Optional[str]:
    """Zenn 記事ディレクトリから最新の日本語記事のパスを取得する。"""
    files = [
        f for f in glob.glob(os.path.join(config.ARTICLES_DIR, "*.md"))
        if not f.endswith(".en.md")
    ]
    if not files:
        return None
    # 更新日時順にソートして最新を取得
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]


def parse_article(file_path: str) -> Tuple[str, str, Optional[str], Optional[str], Optional[str]]:
    """Zenn のマークダウンファイルからタイトル、本文、メタデータを抽出する。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # regexを使用してフロントマターを解析
    title = get_yaml_str(content, 'title')
    if title is None:
        title = "No Title"

    x_viral_post = get_yaml_str(content, 'x_viral_post')
    note_intro = get_yaml_str(content, 'note_intro')
    image_prompt = get_yaml_str(content, 'image_prompt')

    # 本文を取り出すためにフロントマターを除去
    body = strip_yaml_frontmatter(content)

    return title, body, x_viral_post, note_intro, image_prompt


def main() -> None:
    logger.info("--- コンテンツ配信プロセス開始 ---")

    latest_ja_path = get_latest_article()
    if not latest_ja_path:
        logger.warning("配信する記事が見つかりませんでした。")
        return

    # 日本語記事の処理
    title, body, x_viral_text, note_intro_text, image_prompt_text = parse_article(latest_ja_path)
    slug = os.path.basename(latest_ja_path).replace(".md", "")
    zenn_url = f"https://zenn.dev/shironaganegi/articles/{slug}"
    website_url = f"https://techtrend-watch.com/posts/{slug}/"
    
    logger.info(f"処理中 (JA): {title}")

    # 1. Qiita (Bot検出リスクのため一旦無効化)
    # qiita = QiitaPublisher()
    # qiita.publish(title, body, website_url)

    # 2. BlueSky
    bsky = BlueSkyPublisher()
    bsky.publish(title, website_url)

    # 3. Twitter (X)
    twitter = TwitterPublisher()
    twitter.publish(custom_text=x_viral_text, article_url=website_url)

    # 4. Hugo (JA)
    hugo = HugoPublisher()
    hugo.save_article(title, body, website_url, latest_ja_path, lang="ja")

    # 5. Hugo (EN)
    filename_en = os.path.basename(latest_ja_path).replace(".md", ".en.md")
    latest_en_path = os.path.join(config.EN_ARTICLES_DIR, filename_en)
    
    if os.path.exists(latest_en_path):
        logger.info(f"英語版記事が見つかりました: {latest_en_path}")
        try:
            with open(latest_en_path, 'r', encoding='utf-8') as f:
                en_content = f.read()
            
            en_title = get_yaml_str(en_content, 'title')
            if en_title is None:
                en_title = title
            en_body = strip_yaml_frontmatter(en_content)
            
            hugo.save_article(en_title, en_body, website_url, latest_en_path, lang="en")
        except Exception as e:
             logger.error(f"Hugo記事の生成(EN)に失敗: {e}")
    else:
        logger.info("英語版記事が見つからないため、EN配信をスキップします。")

    # 6. Discord 通知
    discord = DiscordPublisher()
    x_text_for_discord = x_viral_text if x_viral_text else f"記事公開: {title}"
    note_text_for_discord = note_intro_text if note_intro_text else "Note用の紹介文はありません。"
    img_text_for_discord = image_prompt_text if image_prompt_text else "画像提案はありません。"
    
    discord.notify(title, website_url, x_text_for_discord, note_text_for_discord, img_text_for_discord)
    
    logger.info("--- コンテンツ配信プロセス完了 ---")


if __name__ == "__main__":
    main()
