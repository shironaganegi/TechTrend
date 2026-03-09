"""
アフィリエイトマネージャー: 記事コンテンツに最適なアフィリエイト商品を
推薦し、HTMLを生成するモジュール。
"""
import json
import random
import os
import logging
from typing import List, Dict, Any

from src.agent_analyst.product_recommender import search_related_items
from src.shared.config import config

logger = logging.getLogger(__name__)


class AffiliateManager:
    """記事コンテンツに基づいてアフィリエイト商品を推薦するクラス。"""

    def __init__(self) -> None:
        self.books_db: Dict[str, Any] = self._load_books_db()

    def _load_books_db(self) -> Dict[str, Any]:
        """技術書データベース (JSON) を読み込む。"""
        db_path = os.path.join(config.DATA_DIR, "technical_books.json")
        try:
            if os.path.exists(db_path):
                with open(db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"技術書DBの読み込みに失敗: {e}")
        return {}

    def get_recommendations(self, article_text: str, keywords: List[str], limit: int = 3) -> str:
        """
        推奨商品のHTMLを返す。
        優先順位:
        1. 記事内容にマッチする技術書
        2. 楽天キーワード検索
        3. フォールバック（ガジェット）
        4. 緊急リンク
        """
        html_output = ""

        # 1. 技術書の検索
        found_books = self._search_books(article_text, keywords)
        if found_books:
            logger.info(f"関連書籍を発見: {found_books[:limit]}")
            for book_kw in found_books[:limit]:
                items = search_related_items(book_kw)
                if items:
                    html_output += "".join(items)
        
        if len(html_output) > 200:
            return self._wrap_output(html_output)

        # 2. キーワード検索
        for kw in keywords[:2]:
            items = search_related_items(kw)
            if items:
                html_output += "".join(items)
        
        if len(html_output) > 200:
            return self._wrap_output(html_output)

        # 3. フォールバック（ガジェット）
        fallback_items = ["ロジクール マウス", "Anker 充電器", "USB-C ケーブル"]
        for fb in fallback_items:
            items = search_related_items(fb)
            if items:
                html_output += "".join(items)
                break
        
        # 4. 緊急リンク
        if not html_output:
            html_output = """
### 👇 エンジニアにおすすめのサービス 👇
[**🌐 独自ドメイン取得なら「お名前.com」。TechTrend Watchも使っています！**](https://www.onamae.com/)
"""
        return self._wrap_output(html_output)

    def _search_books(self, text: str, keywords: List[str]) -> List[str]:
        """記事テキストとキーワードに基づいて、DBから関連書籍名を検索する。"""
        candidates: List[str] = []
        text_lower = text.lower()
        
        for category, books in self.books_db.items():
            if category.lower() in text_lower or any(category.lower() in k.lower() for k in keywords):
                for book in books:
                    candidates.append(book["keyword"])
        
        random.shuffle(candidates)
        return candidates

    def _wrap_output(self, html: str) -> str:
        """アフィリエイトHTMLを装飾されたコンテナで囲む。"""
        wrapped_html = f"""
<div class="recommend-container">
    <div class="recommend-header">📖 関連のおすすめ商品・ツール</div>
    {html}
</div>
"""
        return f"\n<!-- AFFILIATE_START -->\n{wrapped_html}\n<!-- AFFILIATE_END -->\n"



# シングルトンインスタンス
affiliate_manager = AffiliateManager()
