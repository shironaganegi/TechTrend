"""
商品レコメンダー: 楽天API等を利用して、記事キーワードに関連する
アフィリエイト商品を検索するモジュール。
"""
import logging
from typing import List, Optional, Dict, Any
from src.shared.config import config
from src.shared.utils import safe_requests_get

logger = logging.getLogger(__name__)


def _search_rakuten(keyword: str) -> List[str]:
    """
    楽天市場商品検索APIでキーワード検索を行い、
    Zenn互換のMarkdown形式で商品リストを返す。
    """
    if not config.RAKUTEN_APP_ID:
        logger.warning("RAKUTEN_APP_ID が未設定です。楽天検索をスキップします。")
        return []

    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170426"
    params: Dict[str, Any] = {
        "applicationId": config.RAKUTEN_APP_ID,
        "affiliateId": config.RAKUTEN_AFFILIATE_ID,
        "keyword": keyword,
        "format": "json",
        "hits": 3,
        "sort": "reviewCount"
    }

    response = safe_requests_get(url, params=params, timeout=10)
    if not response:
        return []
    
    try:
        data = response.json()
    except Exception as e:
        logger.error(f"楽天APIレスポンスの解析に失敗: {e}")
        return []
    
    items = data.get("Items", [])
    if not items:
        logger.info(f"キーワード '{keyword}' に該当する商品が見つかりませんでした。")
        if "error" in data:
            logger.warning(f"楽天APIエラー: {data}")
        return []

    markdown_results: List[str] = []
    for item_wrapper in items:
        item = item_wrapper.get("Item", {})
        name = item.get("itemName", "")
        price = item.get("itemPrice", "")
        affiliate_url = item.get("affiliateUrl", "")
        image_urls = item.get("mediumImageUrls", [{}])
        image = image_urls[0].get("imageUrl", "") if image_urls else ""
        
        # Zenn 互換の Markdown 形式
        markdown = f"\n[![{name}]({image})]({affiliate_url})\n[{name}]({affiliate_url}) (価格: {price}円)\n"
        markdown_results.append(markdown)

    return markdown_results


def _search_amazon(keyword: str) -> List[str]:
    """
    Amazon Product Advertising API のプレースホルダー。
    PA-APIキーが取得でき次第実装する。
    """
    return []


def search_related_items(keyword: str) -> List[str]:
    """
    複数プラットフォームから商品検索結果を統合して返す。
    """
    logger.info(f"商品検索中: {keyword}")
    results: List[str] = []
    results.extend(_search_rakuten(keyword))
    results.extend(_search_amazon(keyword))
    return results
