"""
失敗事例マイナー: Reddit等からツールに対するネガティブフィードバックや
代替案の情報を収集し、記事に深みを与えるコンテキストを生成するモジュール。
"""
import logging
import urllib.parse
from typing import List
import feedparser

logger = logging.getLogger(__name__)

# ユーザーエージェント (Reddit RSS のスクレイピング用)
_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def mine_failures(tool_name: str) -> str:
    """
    Reddit RSS 検索を利用して、ツールに関するネガティブフィードバック、
    代替案、問題点などを収集する。
    
    Args:
        tool_name: 検索対象のツール名
    Returns:
        収集した投稿のサマリーテキスト
    """
    queries = [
        f"{tool_name} alternative",
        f"{tool_name} sucks",
        f"{tool_name} problem",
        f"{tool_name} vs"
    ]
    
    found_posts: List[str] = []
    logger.info(f"失敗事例の収集を開始: {tool_name}")
    
    for query in queries:
        encoded_query = urllib.parse.quote(query)
        rss_url = f"https://www.reddit.com/search.rss?q={encoded_query}&sort=relevance&t=year"
        
        try:
            feed = feedparser.parse(rss_url, agent=_USER_AGENT)
            for entry in feed.entries[:2]:
                found_posts.append(f"- [Reddit] {entry.title}: {entry.link}")
        except Exception as e:
            logger.warning(f"Reddit スクレイピングエラー (query='{query}'): {e}")
            
    if not found_posts:
        return "No significant negative feedback found (or tool is too new)."
        
    # 重複排除
    unique_posts = list(set(found_posts))
    return "\n".join(unique_posts)


if __name__ == "__main__":
    from src.shared.utils import setup_logging
    setup_logging(__name__)
    print(mine_failures("cursor editor"))
