from datetime import datetime, timedelta

import src.agent_analyst.candidate_selector as candidate_selector


def test_select_best_candidate_excludes_recent_cooldown(monkeypatch):
    recent_date = (datetime.now() - timedelta(days=1)).isoformat()
    old_date = (datetime.now() - timedelta(days=20)).isoformat()

    history = [
        {"name": "recent-tool", "url": "https://example.com/recent", "date": recent_date},
        {"name": "old-tool", "url": "https://example.com/old", "date": old_date},
    ]
    monkeypatch.setattr(candidate_selector, "load_history", lambda: history)

    data = [
        {"name": "recent-tool", "url": "https://example.com/recent", "daily_stars": 100, "source": "github"},
        {"name": "other-tool", "url": "https://example.com/other", "daily_stars": 50, "source": "github"},
    ]

    result = candidate_selector.select_best_candidate(data)
    assert result is not None
    assert result["url"] != "https://example.com/recent"


def test_select_best_candidate_fallback_when_all_recent(monkeypatch):
    recent_date = (datetime.now() - timedelta(days=1)).isoformat()
    history = [{"name": "only-tool", "url": "https://example.com/only", "date": recent_date}]
    monkeypatch.setattr(candidate_selector, "load_history", lambda: history)

    data = [{"name": "only-tool", "url": "https://example.com/only", "daily_stars": 10, "source": "github"}]

    result = candidate_selector.select_best_candidate(data)
    assert result is not None
    assert result["url"] == "https://example.com/only"


def test_select_best_candidate_source_diversity(monkeypatch):
    monkeypatch.setattr(candidate_selector, "load_history", lambda: [])

    data = []
    for i in range(5):
        data.append({"name": f"gh-{i}", "url": f"https://example.com/gh{i}", "daily_stars": 10 - i, "source": "github"})
    for i in range(3):
        data.append({"name": f"qiita-{i}", "url": f"https://example.com/qiita{i}", "daily_stars": 5 - i, "source": "qiita"})

    monkeypatch.setattr(candidate_selector.random, "choice", lambda pool: pool)

    result = candidate_selector.select_best_candidate(data)
    # random.choice をモックして final_pool 自体を確認する
    assert len(result) == 4  # github top2 + qiita top2
    sources = {item["source"] for item in result}
    assert sources == {"github", "qiita"}


def test_select_best_candidate_skips_malformed_history_entry(monkeypatch, caplog):
    history = [{"name": "bad", "url": "https://example.com/bad"}]  # date キー欠落
    monkeypatch.setattr(candidate_selector, "load_history", lambda: history)

    data = [{"name": "tool", "url": "https://example.com/tool", "daily_stars": 5, "source": "github"}]

    result = candidate_selector.select_best_candidate(data)
    assert result is not None
    assert result["url"] == "https://example.com/tool"
