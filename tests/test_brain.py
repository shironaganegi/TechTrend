import sys
import os

# プロジェクトのルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent_analyst.brain_connector import brain_connector
from src.shared.config import config

print(f"BASE_DIR: {config.BASE_DIR}")
print("--- Strategic Context (LATEST_BRAIN Summary) ---")
print(brain_connector.get_strategic_context()[:500] + "...")
print("\n--- AdSense SOP ---")
print(brain_connector.get_adsense_sop()[:300] + "...")
