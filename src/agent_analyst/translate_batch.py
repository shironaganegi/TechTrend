"""
一括翻訳: 既存の日本語記事をまとめて英語に翻訳するバッチ処理モジュール。
"""
import os
import glob
import time
import re
import logging
from src.agent_analyst.content_generator import translate_article_to_english
from src.shared.config import config

logger = logging.getLogger(__name__)


def generate_english_for_existing() -> None:
    """既存の日本語記事を英語に翻訳し、EN_ARTICLES_DIR に保存する。"""
    articles_dir = config.ARTICLES_DIR
    
    # .en.md でない .md ファイルを取得
    files = [
        f for f in glob.glob(os.path.join(articles_dir, "*.md"))
        if not f.endswith(".en.md") and os.path.basename(f) != ".gitkeep"
    ]
    
    logger.info(f"{len(files)} 件の日本語記事が見つかりました。")

    for file_path in files:
        base_name = os.path.basename(file_path)
        en_filename = base_name.replace(".md", ".en.md")
        en_file_path = os.path.join(config.EN_ARTICLES_DIR, en_filename)
        
        # 既存の翻訳がある場合はスキップ
        if os.path.exists(en_file_path):
            logger.info(f"スキップ: {base_name} (英語版が既に存在)")
            continue
            
        logger.info(f"翻訳中: {base_name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            en_body = translate_article_to_english(content)
            
            if en_body:
                # タイトルの抽出
                title = "Tech Report"
                title_match = re.search(r'^title:\s*"(.*)"', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1) + " (English)"
                
                # 英語版フロントマターの生成
                en_frontmatter = f"""---
title: "{title}"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

"""
                # モデルが付与した可能性のあるマークダウンブロックの除去
                clean_body = re.sub(r'^```markdown\s*', '', en_body, flags=re.MULTILINE)
                clean_body = re.sub(r'```\s*$', '', clean_body, flags=re.MULTILINE)
                
                en_full_content = en_frontmatter + clean_body.strip()

                os.makedirs(config.EN_ARTICLES_DIR, exist_ok=True)
                with open(en_file_path, 'w', encoding='utf-8') as f:
                    f.write(en_full_content)
                logger.info(f"✅ 保存完了: {en_file_path}")
                
                # レートリミット対策 (Free tier: 15 RPM)
                time.sleep(10)
            else:
                logger.warning(f"❌ 翻訳失敗: {base_name} (空のレスポンス)")
                
        except Exception as e:
            logger.error(f"❌ 処理エラー ({base_name}): {e}")


if __name__ == "__main__":
    from src.shared.utils import setup_logging
    setup_logging(__name__)
    generate_english_for_existing()
