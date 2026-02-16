---
name: research-data-organizer
description: Organize research data folders with MECE structure and README files. Use for raw data cleanup.
---

# Research Data Organizer

研究データフォルダをMECE構造で整理し、READMEを追加するスキル。

## When to Use

- 研究データフォルダの整理を頼まれたとき
- 日付付きフォルダ名が散らかっているとき
- READMEがないデータフォルダがあるとき
- 新しいデータカテゴリを追加するとき

## Core Principles

### 1. MECE構造

**Mutually Exclusive, Collectively Exhaustive**

```
raw/
├── {category}/           # カテゴリ名（トップレベル）
│   ├── YYYYMMDD_{desc}/  # 日付はサブフォルダに
│   └── README.md         # 必須
```

**NG例：**
```
raw/
├── 20251020_PINM_Diameter/  # ❌ 日付がトップレベル
├── ltw/                      # ✅ カテゴリ名
```

**OK例：**
```
raw/
├── diameter/                 # ✅ カテゴリ名
│   ├── NMPI1/
│   └── README.md
├── ltw/
│   ├── 20251225-LTW-PI/     # 日付はサブに
│   └── README.md
```

### 2. README.md必須項目

各フォルダに以下を含むREADME.mdを作成：

```markdown
# {folder_name}

（旧: {old_name}）  ← リネーム時のみ

{簡潔な説明}

## 測定日
YYYY年MM月DD日

## サンプル対応表
| フォルダ/ファイル | 内容 |
|-----------------|------|
| ... | ... |

## ファイル命名規則
{パターン説明}

## 測定条件
| 項目 | 値 |
|-----|-----|
| ... | ... |

## 解析結果
→ `publication/{topic}/` を参照
```

### 3. publication/構成

```
publication/{topic}/
├── Figure_{Topic}_{desc}.pdf   # 論文図（600dpi）
├── {topic}_results.csv         # 数値データ
└── README_論文用.md            # 論文用説明書
```

**README_論文用.md必須項目：**
1. 解析日
2. 収録ファイル一覧
3. 主な結果（表形式）
4. Figureキャプション案（日本語・英語）
5. 本文記述例
6. 測定条件・デバイスパラメータ
7. 解析スクリプトへの参照

## Workflow

### Step 1: 現状確認

```bash
ls -la {raw_folder}/
```

### Step 2: README有無チェック

```bash
find {raw_folder} -name "README.md"
```

### Step 3: フォルダ名の整理

日付付き → カテゴリ名にリネーム：

```bash
mv 20251020_PINM_Diameter diameter
```

### Step 4: README作成

各フォルダの内容を確認してREADME.md作成。

### Step 5: 関連スクリプト更新

パス変更があれば`analysis/*.py`を更新。

### Step 6: 不要ファイル削除

```bash
find {folder} -name ".DS_Store" -delete
```

## Examples

### 例1: 日付付きフォルダのリネーム

Before:
```
raw/20251020_PINM_Diameter/
```

After:
```
raw/diameter/
├── NMPI1/
├── PI/
└── README.md  ← 「（旧: 20251020_PINM_Diameter）」を記載
```

### 例2: README追加

```markdown
# xrd

X線回折測定データ

## 測定日
2024年11月26日

## サブフォルダ
| フォルダ | 内容 |
|---------|------|
| 20251126_NM_DNTT/ | DNTT薄膜XRD |
| 20251208_XRD_Parylene/ | Parylene膜XRD |

## 解析結果
→ `publication/xrd/` を参照
```

## Caution

- **元データは絶対に編集しない**（フォルダ名変更はOK）
- リネーム時は旧名をREADMEに記載（トレーサビリティ）
- 解析スクリプトのパス更新を忘れずに
