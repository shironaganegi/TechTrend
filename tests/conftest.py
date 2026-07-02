import os

# テスト収集時に src.agent_analyst.llm の LLMClient() 初期化が
# GEMINI_API_KEY 未設定で例外を投げるのを防ぐためのダミー値。
# 実際に LLM API を呼び出すテストは無いため、値は使用されない。
os.environ.setdefault("GEMINI_API_KEY", "dummy-key-for-tests")
