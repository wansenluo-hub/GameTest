---
name: tech-debt-theme
description: 待办技术债——赛博风配色常量重复定义，需抽成Theme资源
metadata:
  type: project
---

技术债(2026-06-15用户要求单独记):赛博风配色常量目前在每个UI脚本里各定义一份(Shop.gd 和 CharacterCreate.gd 顶部各有 C_BG/C_NEON/C_CYAN/C_TEXT 等),互相重复。

**问题**:
- 配色散落,改一处颜色要改多个文件,容易不一致。
- MainMenu 还停留在旧背景图+默认按钮样式,没套赛博风,全局不统一。

**待办(不急,后面UI场景变多后再做)**:
- 把配色常量抽到统一的 Theme 资源(.tres)或一个 ThemeConfig autoload/常量脚本,所有UI引用同一处。
- 顺手把 MainMenu 套上赛博风,做到全局统一。

触发时机:等核心系统(主场景/事件UI)做出来、UI场景数量上来后一并重构,避免现在过早抽象。

相关:[[progress-shop-flow]] [[project-overview]]
