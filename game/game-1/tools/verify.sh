#!/usr/bin/env bash
# verify.sh —— headless 真实运行 Godot 项目主场景，捕获运行时/编译错误
# 用法: bash tools/verify.sh
# 原理: 正常启动项目(autoload 单例会真正初始化、主场景脚本真正编译)，跑几帧后退出，
#       再 grep 出 SCRIPT ERROR / Parse Error / 资源加载失败。
#       比 --check-only(认不出autoload) 和 SceneTree脚本(autoload不初始化) 都可靠。
# 注意: 只能验证"被加载到的脚本"(主场景及其依赖+autoload)。验证某个UI场景时，
#       可临时把它设为主场景，或用 --quit-after 配合切场景。见下方 SCENE 可选参数。
set -u
GODOT="/c/Users/19061/Downloads/Godot_4.6.3/Godot_v4.6.3-stable_win64_console.exe"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCENE="${1:-}"   # 可选: 指定要跑的场景, 如 scenes/ui/Shop.tscn

if [ ! -f "$GODOT" ]; then
  echo "❌ 找不到 Godot: $GODOT"
  echo "   请确认已解压到该路径，或修改本脚本顶部的 GODOT 变量。"
  exit 1
fi

cd "$PROJECT_DIR" || exit 1

if [ -n "$SCENE" ]; then
  echo "▸ 运行场景: $SCENE"
  LOG="$(timeout 90 "$GODOT" --headless --path . --quit-after 5 "res://$SCENE" 2>&1)"
else
  echo "▸ 运行主场景验证项目: $PROJECT_DIR"
  LOG="$(timeout 90 "$GODOT" --headless --path . --quit-after 5 2>&1)"
fi

ERRORS="$(echo "$LOG" | grep -iE "SCRIPT ERROR|Parse Error|Compile Error|Failed to load|Cannot open|Invalid call|Nonexistent" )"

if [ -n "$ERRORS" ]; then
  echo "❌ 发现错误:"
  echo "$ERRORS"
  exit 1
else
  echo "✅ 运行成功，未发现脚本/资源错误。"
  echo "$LOG" | grep -iE "initialized|items:" | sed 's/^/   /'
  exit 0
fi
