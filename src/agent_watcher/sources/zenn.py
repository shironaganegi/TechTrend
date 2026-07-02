import json
from datetime import datetime
from bs4 import BeautifulSoup
from src.shared.utils import setup_logging, safe_requests_get

logger = setup_logging(__name__)

ZENN_ARTICLES_URL = "https://zenn.dev/articles"
ZENN_BASE_URL = "https://zenn.dev"


def fetch_zenn_trends():
    """
    Zenn.dev のトレンド記事を取得する。

    Zenn は CSS モジュールでクラス名がビルド毎にハッシュ化されるため、
    DOM セレクタ依存は壊れやすい。代わりにページ埋め込みの
    __NEXT_DATA__ (Next.js の JSON) から記事情報を抽出する。
    """
    url = ZENN_ARTICLES_URL
    logger.info(f"Fetching Zenn trends: {url}")

    response = safe_requests_get(url)
    if not response:
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        next_data = soup.find('script', id='__NEXT_DATA__')
        if not next_data or not next_data.string:
            logger.warning("Zenn: __NEXT_DATA__ が見つかりません (サイト構造変更の可能性)")
            return []
        data = json.loads(next_data.string)
    except Exception as e:
        logger.error(f"Failed to parse Zenn data: {e}")
        return []

    # __NEXT_DATA__ 内から記事オブジェクト(title/slug/path を持つ dict)を
    # 再帰的に収集する。slug で重複排除。
    seen_slugs = set()
    found = []

    def walk(node):
        if isinstance(node, dict):
            if 'slug' in node and 'title' in node and 'path' in node:
                slug = node.get('slug')
                if slug not in seen_slugs:
                    seen_slugs.add(slug)
                    found.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)

    articles = []
    for item in found[:15]:  # Top 15 trends
        title = item.get('title')
        path = item.get('path')
        if not title or not path:
            continue

        liked = item.get('likedCount') or 0
        user = item.get('user')
        owner = user.get('username') if isinstance(user, dict) else None

        articles.append({
            "source": "zenn",
            "name": title,
            "owner": owner or "Zenn Authors",
            "url": f"{ZENN_BASE_URL}{path}",
            "description": title,
            # ベーススコア50 + いいね数。daily_stars>0 のフィルタを通しつつ
            # 人気記事ほど上位にランクされるようにする。
            "stars": 50 + liked,
            "daily_stars": 50 + liked,
            "language": "japanese",
            "fetched_at": datetime.now().isoformat()
        })

    if not articles:
        logger.warning("Zenn: 記事を抽出できませんでした")

    return articles
