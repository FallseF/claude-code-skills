# Claude Code Skills & Config

Claude Code の自作スキル、コマンド、フック、ターミナル設定をまとめたリポジトリ。
他の端末でも同じ環境を再現できるようにするためのもの。

## 構成

```
.
├── skills/                     # Claude Code カスタムスキル
│   ├── analyze-publish/        # 研究データ解析→論文用パッケージ作成
│   ├── html-to-pdf/            # HTML→PDF変換（Chrome headless）
│   ├── humanize-ja/            # AI文章→自然な日本語にリライト
│   ├── nanobanana/             # Gemini API 画像生成
│   ├── research-data-organizer/# 研究データMECE構造整理
│   └── skill-creator/          # 新スキル作成テンプレート
├── commands/                   # Claude Code スラッシュコマンド
│   ├── otft-analysis.md        # OTFT特性解析（B1500A）
│   └── shuuketsu.md            # マルチエージェント集結
├── hooks/                      # Claude Code フック
│   └── notify-permission.sh    # 承認待ち通知（iPhone/mac/Ghostty）
├── config/                     # Claude Code 設定ファイル
│   ├── CLAUDE.md               # グローバル指示書
│   ├── AGENTS.md               # エージェント向け指示書
│   └── settings.json           # 設定（トークンは要差し替え）
├── terminal/                   # ターミナル設定
│   ├── ghostty/config          # Ghostty（One Dark テーマ）
│   ├── tmux.conf               # tmux（Ctrl+s prefix, vim風移動）
│   └── zellij/config.kdl       # zellij（vim風キーバインド）
├── keyboard/                   # キーボード設定
│   └── karabiner.json          # Karabiner-Elements
└── install.sh                  # インストールスクリプト
```

## セットアップ

```bash
git clone https://github.com/FallseF/claude-code-skills.git
cd claude-code-skills
chmod +x install.sh
./install.sh
```

既存ファイルは上書きされない（SKIPされる）。

## スキル一覧

| スキル | 用途 | トリガー |
|--------|------|----------|
| analyze-publish | 研究データ解析→論文図・READMEパッケージ作成 | `/analyze-publish [path]` |
| html-to-pdf | HTMLファイルのPDF変換 | `PDFに変換して` |
| humanize-ja | AI生成日本語のリライト | `/humanize-ja [file]`, `リライトして` |
| nanobanana | Gemini APIで画像生成 | `/nanobanana`, `画像を作って` |
| research-data-organizer | 研究データフォルダのMECE整理 | `データ整理して` |
| skill-creator | 新しいスキルの対話的作成 | `スキルを作りたい` |

## コマンド一覧

| コマンド | 用途 |
|----------|------|
| `/otft-analysis` | B1500A測定データからOTFT特性を解析 |
| `/shuuketsu` | マルチエージェントカシラシステム起動 |

## 必要な環境変数

```bash
# nanobanana用
export GEMINI_API_KEY="your-gemini-api-key"

# settings.json内のSupabase MCP用
# settings.jsonの<YOUR_SUPABASE_ACCESS_TOKEN>を差し替え
```

## 使用プラグイン

| プラグイン | ソース | 用途 |
|-----------|--------|------|
| commit-commands | claude-plugins-official | コミット・プッシュ・PR |
| pr-review-toolkit | claude-plugins-official | PRレビュー |
| frontend-design | claude-plugins-official | フロントエンドUI生成 |
| security-guidance | claude-plugins-official | セキュリティガイダンス |
| claude-mem | thedotmack | 永続メモリ |
| ralph-loop | claude-plugins-official | ループ実行 |
| decomposition | kuu-marketplace | タスク分解 |

## ライセンス

個人用設定ファイル。自由に参考にしてください。
