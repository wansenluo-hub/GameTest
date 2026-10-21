---
name: progress-shop-flow
description: 商店购物流程开发进度（2026-06-15实现）
metadata:
  type: project
---

2026-06-15 实现了「新游戏→角色创建→商店购物」完整流程。

数据管线（关键，幂等可重跑）：
- tools/build_items.py：读取 ..\..\tupian\商店物品图标\物品说明.xlsx，输出 data/items.json（31物品，含id/category/price/weight/6状态effects/special/risk/icon路径）；把 F1-F31.png 缩略到256x256存 assets/images/icons/items/；往 localization/zh.json+en.json 注入 item.*.name/desc 和 ui.shop.*/ui.character_create.* 共78key。改xlsx后重跑此脚本即可。
- 物品英文id/英文名/分类(food/water/medical/gear)/双语desc 硬编码在 build_items.py 的 META 字典里。

新增代码：
- scripts/core/DataManager.gd（新autoload，已注册project.godot）：get_item/get_all_items/get_items_by_category
- GameManager.gd 扩展：money/inventory/current_weight 字段，has_save()、can_afford()、buy_item()、get_owned_count()；start_new_game按难度initial_money初始化money
- scripts/ui/CharacterCreate.gd + scenes/ui/CharacterCreate.tscn：名字2-12字符校验+难度切换按钮+开始→start_new_game→切Shop。出发日期暂用默认2030-06-15(日期选择待后续)
- scripts/ui/Shop.gd + scenes/ui/Shop.tscn：顶栏金钱/负重，5分类筛选(全部/食物/饮水/医疗/工具装备)，代码动态生成物品卡片(图标+名+效果emoji预览+价格+已购数+购买按钮)，买不起禁用按钮，"出发"按钮暂返回主菜单
- MainMenu.gd：新游戏→CharacterCreate；无存档时ContinueBtn置灰

未验证：本机无Godot CLI，仅做了静态检查(JSON有效、key齐全、节点路径与脚本一致、API枚举名正确)。需用户在Godot 4.6编辑器打开实测，首次会触发图标导入。

待办/简化项：出发日期选择未做；完整存读档未做(has_save仅检查user://savegame.save是否存在)；"出发"后的主游戏场景未做；手写tscn的uid若编辑器报错可删uid行让Godot重生成。

UI风格(2026-06-15二次迭代)：用户要求参考 cyberhiking.com 做"高大上"，并要求物品卡片标注作用(治疗疾病/恢复/副作用)。该网站我端无法访问(WebFetch域名安全拦截)。已选定**深黑(#0a0e0c)+青绿霓虹(#39ff14)+青(#00e5c0)** 赛博风：
- Shop.gd 全部用代码生成StyleBoxFlat霓虹边框，卡片现显示 图标+名称(霓虹绿)+状态effects(emoji)+special作用说明(青色▹)+risk副作用(红色⚠)+价格(金)+已购数+购买按钮(买不起禁用变红框)。网格3列，卡片250x360。
- CharacterCreate.gd 同步套用赛博风(_apply_theme)，难度按钮选中高亮，diff_label显示该难度初始资金$。
- special/risk字段目前仅中文(数据已在items.json)，英文翻译留待内容填充阶段。
配色常量在两个脚本顶部各定义一份(C_BG/C_NEON/C_CYAN等)，若后续要统一可抽到Theme资源。

窗口设置(2026-06-15)：原project.godot无[display]段导致默认窗口1152x648不铺满屏。已加[display]：viewport 1920x1080、window/size/mode=2(最大化启动)、stretch/mode=canvas_items、aspect=keep。UI随窗口缩放自适应。

配色二次校准(参考 tupian/案例/ 4张微信图片)：程序分析得案例图特征——近纯黑底(平均亮度16-24/255,70-92%纯黑)+青翡翠绿点缀(#008060/#006040系,偏冷不刺眼)+白/灰白文字(#e0e0e0)+少量冷蓝紫辅助。据此把主霓虹从刺眼亮绿#39ff14改为青翡翠#00e5c0，背景压到#05080a近纯黑，卡片名称改用白字C_TEXT，绿色只用于描边/高亮。案例图本身用Read工具无法显示(只能程序化分析色彩)。

MainMenu仍是旧背景图+默认按钮样式，未套赛博风(暂未统一)。

商店布局改版(2026-06-15)：用户要求物品独占整行上下排列(非网格)。Shop.tscn的Grid节点从GridContainer改为VBoxContainer(@onready类型同步改VBoxContainer，否则报错)，ScrollContainer加horizontal_scroll_mode=0。_make_card改为横向条目：左96x96图标+中信息区(名称+效果emoji同行,下方青色special作用/红色risk副作用)+右160px固定宽(价格/已购/购买按钮)。

图标去白底(2026-06-15)：用户觉得F30(原本就是RGBA透明)去白底后更好看。在build_items.py加remove_white_bg()：从四边对接近白(RGB>=238)且与边缘连通的像素BFS泛洪转透明(保留物品内部白色不挖空)，再对轮廓残留的抗锯齿白边按接近白程度做半透明羽化(消除深色背景上的白边，实测白边从14-32%降到0%)。已带alpha的图(F30)跳过。流程:原图→缩512→去白底→缩256→居中贴透明画布。31张全部成功,透明占比67-84%。重跑build_items.py即可重新生成。

相关：[[current-progress]] [[project-overview]]
