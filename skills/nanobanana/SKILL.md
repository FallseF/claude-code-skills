---
name: nanobanana
description: Nano Banana（Gemini）で画像生成。「画像を作って」「イメージを生成」「nanobanana」等で発火
user_invocable: true
---

# Nano Banana 画像生成スキル

Gemini の画像生成機能「Nano Banana」を使って、テキストから画像を生成するスキルや。

## 使い方

### 基本的な画像生成

```bash
# Flashモデル（高速・最安 $0.039/枚）
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "富士山と桜の風景画"

# Proモデル（高品質・日本語対応 $0.134〜$0.24/枚）
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "サイバーパンクな東京の夜景" --model pro
```

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--model` | `flash`（高速）or `pro`（高品質） | flash |
| `--output` | 出力ファイルパス | ~/Pictures/ClaudeCode/generated_image.png |
| `--input` | 編集する元画像（編集モード時のみ） | なし |
| `--aspect-ratio` | アスペクト比（1:1, 16:9, 9:16, 4:3, 3:4, 21:9等） | 1:1 |
| `--size` | 解像度（1k, 2k, 4k） | 1k |

### 使用例

```bash
# ワイドアスペクト比で生成
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "海辺の夕日" --aspect-ratio 16:9

# 高解像度で生成
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "宇宙飛行士" --size 2k

# 既存画像を編集
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "背景を夕焼けに変更" --input photo.jpg

# 出力先を指定
python ~/.claude/skills/nanobanana/scripts/generate_nanobanana.py "かわいい猫" --output ~/Pictures/cat.png
```

## セットアップ

1. [Google AI Studio](https://aistudio.google.com/apikey) でAPIキー取得（無料）
2. 環境変数を設定:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
   または `.env` ファイルに `GEMINI_API_KEY=xxx` を記述
3. 依存パッケージをインストール:
   ```bash
   pip install google-genai
   ```

## 料金目安

| モデル | 1枚あたり | 特徴 |
|--------|----------|------|
| Flash | $0.039 | 高速、コスパ最強 |
| Pro | $0.134〜$0.24 | 高品質、日本語プロンプト対応良好 |

## 注意事項

- 生成画像には透かしが入る場合がある
- 人物の顔生成は制限される場合がある
- 商用利用についてはGoogle AI Studioの利用規約を確認
