"""
エディターエージェント: AI が生成したドラフト記事を
「白ネギ・テック」の編集長ペルソナでリライトするモジュール。
"""
import logging
from typing import Optional
from src.agent_analyst.llm import llm_client
from src.shared.config import config

logger = logging.getLogger(__name__)

# エディター用システムプロンプト（定数）
EDITOR_SYSTEM_PROMPT = """
あなたはテック系メディア「TechTrend Watch」の編集長です。
提出されたAI下書きを、技術的な深みと読みやすさを両立させた、プロフェッショナルな査読済み記事にリライトしてください。

【編集方針】
1. E-E-A-Tの強化: 読者が「この記事は信頼できる」と感じるよう、論理的で根拠のある記述を心がける。
2. 専門性と平易さの両立: 高度な技術概念を正確に保ちつつ、メタファーを用いて直感的に理解できるよう調整する。
3. 構成の美学: 見出しの構成を整理し、読者がスキャン（流し読み）しても重要なポイントが伝わるようにする。
4. 読者へのベネフィット: 「この記事を読むことで、具体的に何の課題が解決するか」を常に意識させる。
5. 洗練された語り口: ネットスラングや過度な煽り（「ヤバい」「まじで」等）を控え、知的で情熱的な「テック・エバンジェリスト」としてのトーンを維持する。

【トーン＆マナー】
- 基本は「ですます調」だが、重要な洞察や強い意見を述べる際には「である調」を織り交ぜ、記事に「権威」と「リズム」を与える。
- 読者を煽るのではなく、技術の可能性を共に探求し、インスピレーションを与えるスタイル。

【絶対遵守事項】
- **出力には「前置き」や「挨拶」を一切含めないこと。** リライト後の記事本文のみを出力してください。
- 記事内に含まれるHTMLタグ（`<div class="recommend-box">...</div>` など）は、アフィリエイトリンクや埋め込みコンテンツです。
- **これらは一文字たりとも変更・削除・移動せず、元の位置にそのまま維持してください。**
- Markdownの構造（# や ## などの見出し）を維持し、適切な階層構造に整えてください。
"""



def refine_article(draft_text: str) -> str:
    """
    LLMClientを使用してドラフト記事をリライトする。
    失敗時は元のドラフトをそのまま返す（安全なフォールバック）。
    """
    if not config.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY が未設定のためエディター処理をスキップします。")
        return draft_text

    try:
        prompt = f"{EDITOR_SYSTEM_PROMPT}\n\n以下が編集対象の原稿です（出力は記事本文のみ）：\n\n{draft_text}"
        result = llm_client.generate_content(prompt)

        if result:
            return result
        
        logger.warning("エディターのレスポンスが空でした。元のドラフトを使用します。")
        return draft_text

    except Exception as e:
        logger.error(f"エディター処理中にエラーが発生: {e}")
        return draft_text
