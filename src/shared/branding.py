"""サイト全体で共有するブランディング定数。

運営者名・ベースURL 等、複数モジュール（生成パイプラインと一括是正スクリプト）から
参照される値を一箇所に集約する。運営者名を変更する場合はここだけを編集する。
"""

# サイトの公開ベースURL（末尾スラッシュなし）
SITE_BASE_URL = "https://techtrend-watch.com"

# 運営者／編集者の表示名（実在するハンドル）。
# frontmatter の author、著者ボックス、hugo.toml の既定 author に使用する。
SITE_AUTHOR = "しろねぎ"

# 著者プロフィールページの slug（/authors/<slug>/ に対応）
SITE_AUTHOR_SLUG = "shironaganegi"
