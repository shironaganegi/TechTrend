"""トレンドデータの読み込みと、記事化する候補の選定を行うモジュール。"""
from datetime import datetime, timedelta
import os
import json
import random

from src.shared.config import config
from src.shared.utils import setup_logging

logger = setup_logging(__name__)


def load_history():
    history_path = os.path.join(config.DATA_DIR, "history.json")
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_history(tool_name, url):
    history_path = os.path.join(config.DATA_DIR, "history.json")
    history = load_history()
    history.append({
        "name": tool_name,
        "url": url,
        "date": datetime.now().isoformat()
    })
    # Keep only last 100 entries
    history = history[-100:]
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def load_trends_data():
    """Loads the latest trends JSON file from the data directory."""
    data_dir = config.DATA_DIR
    if not os.path.exists(data_dir):
        return []

    files = sorted([f for f in os.listdir(data_dir) if f.startswith("trends_")], reverse=True)
    if not files:
        return []

    latest_file = os.path.join(data_dir, files[0])
    logger.info(f"Loading data from {latest_file}")

    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def select_best_candidate(data):
    """Selects the best tool to write about, considering history and diversity."""
    history = load_history()
    cooldown_period = timedelta(days=14)
    cutoff_date = datetime.now() - cooldown_period

    recent_posted_urls = []
    for h in history:
        try:
            post_date = datetime.fromisoformat(h['date'])
            if post_date > cutoff_date:
                recent_posted_urls.append(h['url'])
        except (ValueError, KeyError):
            logger.warning(f"Skipping malformed history entry: {h}")
            continue

    candidates = [item for item in data if item.get('daily_stars', 0) > 0 and item.get('url') not in recent_posted_urls]

    # Fallback if everything is filtered
    if not candidates:
        logger.info("All trending topics were posted recently. Picking a random one from top trends anyway.")
        candidates = [item for item in data if item.get('daily_stars', 0) > 0]

    if not candidates:
        return None

    # Ensure Source Diversity (Pick top 2 from each source)
    candidates_by_source = {}
    for item in candidates:
        src = item.get('source', 'unknown')
        if src not in candidates_by_source:
            candidates_by_source[src] = []
        candidates_by_source[src].append(item)

    final_pool = []
    for src, items in candidates_by_source.items():
        sorted_items = sorted(items, key=lambda x: x.get('daily_stars', 0), reverse=True)
        final_pool.extend(sorted_items[:2])

    logger.info(f"Candidate Poll Size: {len(final_pool)} (Sources: {list(candidates_by_source.keys())})")

    return random.choice(final_pool)
