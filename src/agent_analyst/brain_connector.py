"""
Brain Connector: 外部の戦略ドキュメント (brain/) から最新の知見を読み取り、
AIエージェントに提供するためのモジュール。
"""
import os
import logging
from src.shared.config import config

logger = logging.getLogger(__name__)

class BrainConnector:
    def __init__(self) -> None:
        self.brain_dir = os.path.join(config.DATA_DIR, "brain")
        self.latest_brain_path = os.path.join(self.brain_dir, "LATEST_BRAIN.md")
        self.sop_adsense_path = os.path.join(self.brain_dir, "SOP_ADSENSE_APPROVAL.md")

    def get_strategic_context(self) -> str:
        """
        LATEST_BRAIN.md からバズ構造や収益化の要約を抽出して返す。
        """
        if not os.path.exists(self.latest_brain_path):
            logger.warning(f"Brain file not found: {self.latest_brain_path}")
            return "No strategic data available."

        try:
            with open(self.latest_brain_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 要約セクションのみを抽出（あるいは冒頭の数KB）
            # ここではプロンプトを圧迫しすぎないよう、重要なバズ構造とアフィ情報の要約を優先
            strategic_blocks = []
            
            # 各セクションの冒頭要約を取得（## 🔹 ... の後の数行）
            import re
            sections = re.split(r'## 🔹 ', content)
            for section in sections[1:5]: # 最初の5セクション程度
                lines = section.split("\n")
                header = lines[0]
                # 箇条書きや要約部分を抽出
                summary = "\n".join(lines[1:15]) # セクション内の要約部分を切り出す
                strategic_blocks.append(f"【{header}】\n{summary}")

            return "\n\n".join(strategic_blocks)
        except Exception as e:
            logger.error(f"Failed to read brain context: {e}")
            return "Error reading strategic brain."

    def get_adsense_sop(self) -> str:
        """
        AdSense 審査合格のためのSOP要件を返す。
        """
        if not os.path.exists(self.sop_adsense_path):
            return "Ensure 1500+ words, original insights, and essential pages (Privacy, About, Terms)."

        try:
            with open(self.sop_adsense_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read SOP: {e}")
            return "Error reading SOP."

brain_connector = BrainConnector()
