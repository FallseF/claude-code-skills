# Claude Code 環境セットアップガイド

このアカウントで使っている Claude Code の設定、カスタマイズ、ツール構成の全体像。

---

## 1. Claude Code の基本設定

### CLAUDE.md（グローバル指示書）

`~/.claude/CLAUDE.md` に置くことで、全プロジェクトで適用される指示書。

主なカスタマイズ:

- **言語**: 関西ヤクザ風の口調で応答させている（`settings.json` の `language` フィールド）
- **eval モード**: メッセージ末尾に `eval` と書くと忖度なしの客観評価モードになる
- **askif モード**: メッセージ末尾に `askif` と書くと確認優先モードになる
- **git worktree 必須**: 複数エージェント並列作業時は git worktree を強制
- **TypeScript優先**: 新規ファイルは常にTypeScriptで書く
- **図表スタイル**: Nature風（クリーン、ミニマル、ハイコントラスト）
- **日本語フォント**: IPAexGothic か Noto Sans JP を使用

### AGENTS.md（エージェント向け指示書）

`~/.claude/AGENTS.md` は Codex 等の外部エージェントが読む英語版の指示書。
CLAUDE.md と同じルールを英語で記載。

### settings.json のカスタマイズポイント

```json
{
  "cleanupPeriodDays": 99999,       // 履歴を消さない
  "skipDangerousModePermissionPrompt": true,  // 危険モード確認スキップ
  "language": "昔の関西のヤクザ風の言葉、カシラであるユーザーの舎弟",
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["シノギ中", "根回し中", "仁義通し中", ...]  // スピナーもヤクザ風
  }
}
```

### フック: 承認待ち通知

Claude Code が権限確認で止まったとき、3つのチャネルで通知が飛ぶ:

1. **iPhone**: ntfy.sh 経由のプッシュ通知（トピック: `claude-fba63096`）
2. **macOS**: osascript のネイティブ通知
3. **Ghostty**: ターミナルのエスケープシーケンス通知（クリックでペインに飛べる）

設定場所: `~/.claude/hooks/notify-permission.sh`

---

## 2. ターミナル環境

### Ghostty（メインターミナル）

設定場所: `~/.config/ghostty/config`

| 項目 | 設定値 |
|------|--------|
| テーマ | One Dark（yazi と統一） |
| カーソル色 | #61afef（One Dark blue） |
| パディング | 12px |
| macOS Option | Alt として使用 |
| タブ名変更 | Cmd+R |
| 通知 | デスクトップ通知有効 |

### tmux

設定場所: `~/.tmux.conf`

| 項目 | 設定値 |
|------|--------|
| プレフィックス | `Ctrl+s`（デフォルトの Ctrl+b から変更） |
| マウス | 有効 |
| ペイン分割 | `\|` で横、`-` で縦（分割後に均等化） |
| ペイン移動 | vim風（h/j/k/l） |
| ステータス | PREFIX押下時にマゼンタ表示 |

マルチエージェント作業時に tmux セッションを使う:
- `wakagashira` セッション: 若頭（メインエージェント）
- `multiagent` セッション: 組員（サブエージェント）

### zellij（tmux の代替/併用）

設定場所: `~/.config/zellij/config.kdl`

| 項目 | 設定値 |
|------|--------|
| キーバインド | clear-defaults=true でフルカスタム |
| モード切替 | Ctrl+p (pane), Ctrl+t (tab), Ctrl+n (resize), Ctrl+h (move), Ctrl+s (scroll), Ctrl+o (session) |
| ペイン移動 | vim風（h/j/k/l） |
| tmux互換 | Ctrl+b で tmux風モード有効 |
| ロック | Ctrl+g でロック/アンロック |

---

## 3. キーボード設定

### Karabiner-Elements

設定場所: `~/.config/karabiner/karabiner.json`

| ルール | 動作 |
|--------|------|
| 左Cmd単独 | 英数キー（IMEオフ） |
| 右Cmd単独 | かなキー（IMEオン） |
| CapsLock | 左Control |
| 右Option単独 (MX Keys M Mac のみ) | Fn キー |

US配列キーボードで日本語入力を快適にするための設定。

---

## 4. 使用プラグイン

### 公式プラグイン (claude-plugins-official)

| プラグイン | 用途 |
|-----------|------|
| commit-commands | `git commit` / `git push` / PR作成のワンコマンド化 |
| pr-review-toolkit | PR のコードレビュー、サイレント障害検出、型設計分析等 |
| frontend-design | フロントエンドUI の高品質デザイン生成 |
| security-guidance | セキュリティガイダンス |
| ralph-loop | ループ処理の自動実行 |

### サードパーティプラグイン

| プラグイン | ソース | 用途 |
|-----------|--------|------|
| claude-mem | thedotmack | セッション間の永続メモリ（MCP経由） |
| decomposition | kuu-marketplace | 複雑タスクの詳細分解 |

### MCP サーバー

| サーバー | 用途 |
|----------|------|
| supabase | Supabase プロジェクト管理・SQL実行・Edge Function デプロイ等 |
| codex | OpenAI Codex との連携 |

---

## 5. 自作スキルの詳細

### analyze-publish（研究データ解析）

研究データフォルダを指定して、Nature風の論文用グラフとREADMEパッケージを一括作成する。
推測禁止の7フェーズワークフロー（データ確認→質問→確認→スクリプト作成→実行→README→整理）。

グラフ設定:
- フォント: Arial 8-9pt
- 解像度: 300dpi (画面) / 600dpi (保存)
- シングルカラム: 89mm / ダブルカラム: 183mm
- 軸: 上・右を非表示、FormatStrFormatter('%g') で 0.0→0 変換

### html-to-pdf（HTML→PDF変換）

Chrome headless モードで HTML を PDF に変換。印刷用CSS の自動追加、改ページ制御、背景色保持に対応。

### humanize-ja（AI文章リライト）

AI が生成した日本語テキストの「AIっぽさ」を消して自然な文章にリライトする。
Markdown記法禁止、括弧多用禁止、安全クッション削除など厳密なルールで制御。

### nanobanana（Gemini 画像生成）

Google Gemini API を使った画像生成。Flash（高速・安価 $0.039/枚）と Pro（高品質 $0.134~/枚）の2モデル対応。
アスペクト比変更、解像度選択、既存画像の編集モードあり。

### research-data-organizer（データ整理）

研究データフォルダを MECE（Mutually Exclusive, Collectively Exhaustive）構造で整理。
日付名フォルダ→カテゴリ名フォルダへのリネーム、各フォルダへの README 自動生成。

### skill-creator（スキル作成）

新しい Claude Code スキルを対話的に作成するためのテンプレートとワークフロー。

---

## 6. 新しい端末でのセットアップ手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/FallseF/claude-code-skills.git
cd claude-code-skills

# 2. インストール実行
chmod +x install.sh
./install.sh

# 3. settings.json を手動マージ
# config/settings.json を参考に ~/.claude/settings.json を編集
# SUPABASE_ACCESS_TOKEN を実際の値に差し替え

# 4. 環境変数を設定
echo 'export GEMINI_API_KEY="your-key"' >> ~/.zshrc

# 5. nanobanana の依存パッケージ
pip install google-genai

# 6. ntfy アプリ（iPhone通知用、任意）
# App Store から ntfy をインストール
# トピック claude-fba63096 を購読

# 7. Homebrew パッケージ（dotfiles リポジトリ参照）
# https://github.com/FallseF/dotfiles の Brewfile を使用
```

---

## 7. 関連リポジトリ

| リポジトリ | 用途 |
|-----------|------|
| [FallseF/dotfiles](https://github.com/FallseF/dotfiles) | Brewfile, setup.sh |
| [FallseF/swiss-slides](https://github.com/FallseF/swiss-slides) | Swiss Modern reveal.js スライド生成スキル |
| [FallseF/claude-code-skills](https://github.com/FallseF/claude-code-skills) | このリポジトリ |
