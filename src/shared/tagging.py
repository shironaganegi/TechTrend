"""
タグ導出モジュール: 記事タイトル＋本文から、検索・回遊に役立つ
「具体的なトピックタグ」を導出する。

従来は全記事が ["AI", "Tools"] という汎用タグのみで、特定技術での
ブラウズができなかった。本モジュールで内容に応じた具体タグを付与し、
タグ別ページ(/tags/xxx/)を実用的なナビゲーションにする。

hugo.py（新規記事）と既存記事の一括再タグ付けの両方で共用する。
"""
from typing import List, Optional

# カテゴリタグ -> 判定キーワード（小文字で比較。誤タグを避け保守的に選定）
TAG_KEYWORDS = {
    "LLM": ["llm", "gpt", "gemini", "claude", "大規模言語モデル", "language model"],
    "RAG": ["rag", "検索拡張", "retrieval augmented", "retrieval-augmented"],
    "AIエージェント": ["aiエージェント", "ai agent", " agent ", "autonomous agent", "mcp", "マルチエージェント"],
    "生成AI": ["画像生成", "動画生成", "stable diffusion", "diffusion", "midjourney",
              "flux.1", "音声生成", "テキスト生成", "生成モデル"],
    "機械学習": ["機械学習", "machine learning", "深層学習", "deep learning",
              "ニューラルネット", "推論エンジン", "ファインチューニング", "fine-tuning"],
    "セキュリティ": ["セキュリティ", "脆弱性", "vulnerabilit", "暗号", "認証", "cve",
                "ペネトレ", "pentest", "マルウェア", "ランサムウェア", "exploit"],
    "DevOps": ["docker", "kubernetes", "k8s", "ci/cd", "devops", "コンテナ",
               "デプロイ自動", "terraform", "github actions"],
    "クラウド": ["aws", "gcp", "azure", "クラウド", "serverless", "サーバーレス", "cloudflare"],
    "フロントエンド": ["react", "vue", "svelte", "next.js", "フロントエンド",
                "typescript", "javascript", "tailwind", "web ui"],
    "Python": ["python", "パイソン"],
    "Rust": ["rust言語", " rust ", "rust製"],
    "Go": ["golang", "go言語", "go製"],
    "データベース": ["データベース", "postgres", "mysql", "sqlite", "ベクトルデータベース",
                "vector database", "ベクトルdb", "nosql"],
    "オープンソース": ["オープンソース", "open source", "open-source", "oss"],
}

# 全記事共通のベースタグ（広いカテゴリ）
BASE_TAGS = ["AI", "Tools"]


def derive_tags(title: str, body: str, max_tags: int = 6) -> List[str]:
    """タイトル＋本文から具体的なトピックタグを導出して返す。

    BASE_TAGS を先頭に、内容に一致したカテゴリタグを追加する。
    重複を除き、最大 max_tags 個に制限する。
    """
    text = f"{title}\n{body}".lower()
    tags: List[str] = list(BASE_TAGS)

    for tag, keywords in TAG_KEYWORDS.items():
        if tag in tags:
            continue
        if any(kw.lower() in text for kw in keywords):
            tags.append(tag)

    # 重複排除（順序維持）して上限適用
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:max_tags]
