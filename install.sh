#!/usr/bin/env bash
set -euo pipefail

# Claude Code Skills & Config Installer
# Usage: ./install.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CONFIG_DIR="$HOME/.config"

echo "=== Claude Code Skills & Config Installer ==="
echo ""

# Skills
echo "[1/6] Installing skills..."
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name="$(basename "$skill_dir")"
    target="$CLAUDE_DIR/skills/$skill_name"
    if [ -d "$target" ]; then
        echo "  SKIP: $skill_name (already exists)"
    else
        cp -r "$skill_dir" "$target"
        echo "  OK: $skill_name"
    fi
done

# Commands
echo "[2/6] Installing commands..."
mkdir -p "$CLAUDE_DIR/commands"
for cmd_file in "$SCRIPT_DIR"/commands/*.md; do
    cmd_name="$(basename "$cmd_file")"
    target="$CLAUDE_DIR/commands/$cmd_name"
    if [ -f "$target" ]; then
        echo "  SKIP: $cmd_name (already exists)"
    else
        cp "$cmd_file" "$target"
        echo "  OK: $cmd_name"
    fi
done

# Hooks
echo "[3/6] Installing hooks..."
mkdir -p "$CLAUDE_DIR/hooks"
for hook_file in "$SCRIPT_DIR"/hooks/*; do
    hook_name="$(basename "$hook_file")"
    target="$CLAUDE_DIR/hooks/$hook_name"
    if [ -f "$target" ]; then
        echo "  SKIP: $hook_name (already exists)"
    else
        cp "$hook_file" "$target"
        chmod +x "$target"
        echo "  OK: $hook_name"
    fi
done

# Config (CLAUDE.md, AGENTS.md) - settings.json needs manual merge
echo "[4/6] Installing config files..."
for config_file in CLAUDE.md AGENTS.md; do
    target="$CLAUDE_DIR/$config_file"
    if [ -f "$target" ]; then
        echo "  SKIP: $config_file (already exists)"
    else
        cp "$SCRIPT_DIR/config/$config_file" "$target"
        echo "  OK: $config_file"
    fi
done
echo "  NOTE: settings.json must be merged manually (contains personal tokens)"

# Terminal configs
echo "[5/6] Installing terminal configs..."
# Ghostty
if [ -d "$CONFIG_DIR/ghostty" ]; then
    echo "  SKIP: ghostty/config (directory already exists)"
else
    mkdir -p "$CONFIG_DIR/ghostty"
    cp "$SCRIPT_DIR/terminal/ghostty/config" "$CONFIG_DIR/ghostty/config"
    echo "  OK: ghostty/config"
fi

# tmux
if [ -f "$HOME/.tmux.conf" ]; then
    echo "  SKIP: .tmux.conf (already exists)"
else
    cp "$SCRIPT_DIR/terminal/tmux.conf" "$HOME/.tmux.conf"
    echo "  OK: .tmux.conf"
fi

# zellij
if [ -d "$CONFIG_DIR/zellij" ]; then
    echo "  SKIP: zellij/config.kdl (directory already exists)"
else
    mkdir -p "$CONFIG_DIR/zellij"
    cp "$SCRIPT_DIR/terminal/zellij/config.kdl" "$CONFIG_DIR/zellij/config.kdl"
    echo "  OK: zellij/config.kdl"
fi

# Keyboard
echo "[6/6] Installing keyboard configs..."
if [ -f "$CONFIG_DIR/karabiner/karabiner.json" ]; then
    echo "  SKIP: karabiner.json (already exists)"
else
    mkdir -p "$CONFIG_DIR/karabiner"
    cp "$SCRIPT_DIR/keyboard/karabiner.json" "$CONFIG_DIR/karabiner/karabiner.json"
    echo "  OK: karabiner.json"
fi

echo ""
echo "=== Installation complete ==="
echo ""
echo "Post-install steps:"
echo "  1. Merge config/settings.json into ~/.claude/settings.json manually"
echo "  2. Set your SUPABASE_ACCESS_TOKEN and GEMINI_API_KEY"
echo "  3. Install nanobanana dependency: pip install google-genai"
echo "  4. Install ntfy for iPhone notifications (optional)"
