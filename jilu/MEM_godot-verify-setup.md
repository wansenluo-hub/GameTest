---
name: godot-verify-setup
description: 本机Godot可执行文件路径与headless验证方法
metadata:
  type: reference
---

本机已有 Godot 4.6.3 命令行可用(2026-06-15解决"AI无法运行Godot验证"问题)。

可执行文件(console版,能输出日志)：
D:\Godot\Godot_v4.6.3-stable_win64_console.exe
(目录 D:\Godot 下另有 GUI版 Godot_v4.6.3-stable_win64.exe 和原始 zip。2026-06-15从 Downloads 移到 D:\Godot)

游戏工程根目录：E:\memory\YouXin\game\game-1 (project.godot 所在,tools/脚本相对此目录运行)

验证脚本：game\game-1\tools\verify.sh
- 用法：`bash tools/verify.sh` (跑主场景) 或 `bash tools/verify.sh scenes/ui/Shop.tscn` (跑指定场景)
- 原理：headless 真实运行项目(--headless --path . --quit-after 5)，autoload单例真正初始化、被加载脚本真正编译，再grep出 SCRIPT ERROR/Parse Error/资源错误。已反向测试确认能抓到注入的语法错误。

关键经验(踩过的坑)：
- `--check-only --script xxx.gd` 单脚本检查 **认不出autoload单例**(GameManager/DataManager/Translator)，会误报"Identifier not found"。不要用它验证引用单例的脚本。
- `extends SceneTree` + `--script` 方式 autoload **不初始化**，同样误报。
- 唯一可靠方式=**正常运行项目主场景**(--quit-after N)，autoload会初始化。但只验证"被加载到的脚本"(主场景+依赖+autoload)，验证孤立UI场景要用 verify.sh 的场景参数把它作为主场景跑。
- 改完GDScript/场景后应跑 verify.sh 确认，不再纯靠静态检查或用户手动跑。

相关：[[progress-shop-flow]] [[project-overview]]
