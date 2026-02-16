---
name: skill-creator
description: Create new Claude Skills interactively. Use when user wants to add a custom skill.
---

# Skill Creator

新しいClaudeスキルを対話的に作成するスキル。

## When to Use

- ユーザーが「スキルを作りたい」「スキルを追加したい」と言ったとき
- 繰り返し使うワークフローをスキル化したいとき

## Skill Structure

スキルは以下の構成：

```
~/.claude/skills/{skill-name}/
├── SKILL.md          # 必須：YAMLフロントマター + 説明
├── references/       # 任意：参照ドキュメント
├── scripts/          # 任意：実行スクリプト
└── assets/           # 任意：テンプレート等
```

## SKILL.md Template

```markdown
---
name: my-skill-name
description: A clear description (max 200 chars). Claude uses this to decide when to invoke.
---

# Skill Title

## Overview
What this skill does.

## When to Use
Trigger conditions.

## Workflow
Step-by-step instructions.

## Examples
Usage examples.
```

## Creation Workflow

1. **ヒアリング**: ユーザーにスキルの目的を確認
   - 何をするスキル？
   - いつ使う？
   - 必要なファイル/スクリプトはある？

2. **フォルダ作成**: `~/.claude/skills/{skill-name}/`

3. **SKILL.md作成**: YAMLフロントマター + 詳細説明

4. **追加ファイル**: 必要に応じてreferences/, scripts/を追加

5. **確認**: スキルが正しく認識されるか確認

## Key Points

- **name**: 64文字以内、ハイフン区切り推奨
- **description**: 200文字以内、Claudeがスキル選択に使う
- 日本語OK（ただしnameは英語推奨）

## Reference

- [Agent Skills Docs](https://code.claude.com/docs/en/skills)
- [How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Agent Skills Spec](https://agentskills.io)
