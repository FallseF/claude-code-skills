#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="$(basename "$(pwd)")"
NTFY_TOPIC="claude-fba63096"

# iPhoneに通知（ntfy）
curl -s \
  -H "Title: Claude Code" \
  -H "Tags: robot" \
  -d "承認待ち: ${PROJECT_NAME}" \
  "https://ntfy.sh/${NTFY_TOPIC}" >/dev/null

# macOSにも通知（ローカル）
osascript -e "display notification \"承認待ちやで！\" with title \"Claude Code\" subtitle \"${PROJECT_NAME}\"" 2>/dev/null || true

# Ghosttyに通知（クリックで該当ペインに飛べる）
# サブタイトルはGhosttyが自動でターミナルタイトルを付与
printf '\e]9;入力待ち\a' > /dev/tty 2>/dev/null || true
