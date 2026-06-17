# 📚 Knowledge Indexes (知的資産インデックス)

本ファイルは、プロジェクトを跨いで参照すべき外部ナレッジ（NotebookLM等）および、現在 Antigravity に実装済みの共通スキルのリストです。

## 1. 外部ナレッジ（NotebookLM等）一覧
AIエージェントは「ノートブックで調べて」等の指示があった際、以下のURLを優先的に参照し、最新の知見を取り込んでください。

| ノートブック名 | URL | 内容・用途 |
| :--- | :--- | :--- |
| **AI_Analyst** | https://notebooklm.google.com/notebook/02dd598a-6a87-4944-8b4a-b3de626f38d9 | Antigravityのスキル、SNS自動化、最新AIトレンド、運用戦略 |
| **X_ANALYSIS_POINTS.md** | `d:\ProjectA\brain\X_ANALYSIS_POINTS.md` | **(重要)** Xでの情報分析における着眼点・調査項目チェックリスト |
| **RESEARCH_TARGETS.md** | `d:\ProjectA\brain\RESEARCH_TARGETS.md` | `ProjectA` 各プロジェクトへの具体的な活用・落とし込み案 |
| **SOP_ADSENSE_APPROVAL.md** | `d:\ProjectA\brain\SOP_ADSENSE_APPROVAL.md` | **(重要)** Google AdSense 審査合格のためのブログ制作標準手順書 |

---

## 2. 実装済みグローバルスキル (Global Skills)
`/` コマンドで呼び出し可能な共通ワークフローの一覧です。
保存先: `d:\ProjectA\_agents\workflows\`

| コマンド | スキル名 | 概要 |
| :--- | :--- | :--- |
| `/new-project-setup` | 新規プロジェクト立ち上げ | `GLOBAL_OS.md` に基づいた標準ディレクトリ構造と初期設定を自動生成 |
| `/save-conversation-as-skill` | 会話ログのSkill化 | 現在の会話から成功パターンを抽出し、新しいSkillファイルとして自動保存 |

---

## 3. インデックスの運用ルール
- 新しい NotebookLM を追加した際は、必ずこのファイルの「1. 外部ナレッジ」に追記すること。
- 新しく汎用的な Skill を作成した際は、必ず「2. 実装済みグローバルスキル」に追記すること。
- AIエージェントは各セッションの開始時、`GLOBAL_OS.md` と共にこの `INDEX.md` を読み込み、現在利用可能なリソースを把握すること。
