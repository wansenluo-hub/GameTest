---
name: event-script-format
description: 事件剧本Excel填写格式约定与模板位置
metadata:
  type: project
---

事件剧本采用「单表扁平」结构(用户2026-06-15选定)。模板已生成：E:\memory\YouXin\jilu\事件剧本模板.xlsx，由 game\game-1\tools\build_event_template.py 生成(改约定后重跑)。

模板含3个Sheet：
1. 事件表(用户填)：24列，一行一个事件。必填列(标*)：事件ID、事件类型、事件名称、路段、事件描述。其余可空。三组选项各5列(文本/效果/获得物品/消耗物品/结果文本)。
2. 填写说明：格式规则。
3. 参考字典：状态名、路段、31个物品id中英对照。

填写约定(程序解析依据)：
- 事件类型：major重大(需选择)/minor小事件/auto自动
- 路段id：andes/red_zone/transition/brazil
- 效果列格式：状态名+数值,逗号分隔，如 health+10,stamina-5,money-50。状态名=stamina/energy/food/water/health/temperature/money(对应7状态+钱，注意代码里状态英文名见GameManager)
- 获得/消耗物品列：物品id:数量,逗号分隔，如 jerky:2,antivenom:1。物品id必须匹配items.json(31个)
- 触发条件(可选高级)：health<30 或 has_item:antivenom
- 天数范围如1-120，触发概率0-100

下一步：用户填好事件表→告知AI→AI写转换脚本生成events.json + 事件系统(模块7)+事件UI(模块14)。建议先填10-15个核心事件搭系统。

92事件已导入(2026-06-15)：用户从DeepSeek生成92个事件(13类)，粘贴在 E:\memory\YouXin\新建文本文档.txt。由 tools/import_events.py 解析→修正→写入 事件剧本模板.xlsx 的「事件表」(覆盖示例)。
- 修正的错误：human_001/human_002/river_010/terrain_008 把money+X填进了"获得物品"列，已移到对应"效果"列；andes_009多一空列已删；auto_001~004是14列简化格式(单选项)已补齐24列。
- 事件分布：andes18 red_zone20 transition45 brazil46 all19(含多路段)；major59 minor28 auto5。
- 设计确认(用户)：商店没有的物品=游戏中通过随机事件获取/消耗(战利品/食材/工具)，区别于31个商店补给品。已建「事件物品表」Sheet登记21个事件物品(meat生肉/cooked_meat熟肉/fruit野果/mushroom蘑菇/cocoa_bean可可豆/hot_water温泉水/wood木柴/animal_fur兽皮/fishing_bait鱼饵/phosphor磷光粉/sunglasses墨镜/knife军刀/bullet子弹/flare信号弹/fishing_hook鱼钩/firefly_lantern萤火虫灯/bible小圣经/glowing_fish发光鱼/glowing_water发光水/crab_meat蟹肉/food泛指)，效果和可卖价待定。
- 待办：事件物品效果/售价未定；animal_001选项3等"获得machete"语义存疑(可能想表达"需持有")，做事件系统时与用户复核；92事件尚未关联到321站点的大地标(andes_event_01等占位待对接)。
- 模板Sheet顺序：事件表/站点表/事件物品表/填写说明/参考字典。

收尾(2026-06-15三件事):
1. 事件物品效果/售价已填(tools/fill_event_items.py)：21个事件物品参考商店数值体系定了effect和可卖价。如meat生肉food+20,health-5/$2；cooked_meat熟肉food+30,stamina+5/$4；animal_fur兽皮temperature+5/$8；墨镜$10军刀$15信号弹$12等工具无食用效果"-"。"food"泛指建议事件改具体物品。
2. animal_001"用砍刀对峙"语义复核：machete实际在第21列=消耗物品列(不是获得列)，数据本来就对，之前是AI误读，无需修改。
3. 站点对接缺口(关键)：站点表共61大地标，每个有占位事件ID(andes_event_01..)但现有92事件无一对接(占位ID全空)。92事件中只有7个固定/剧情事件(andes_004源头瀑布、andes_009告别安第斯、season_001雨季第一场雨、auto_001~004路段切换/GPS)，其余85个是随机事件(按路段+概率触发，可复用，不绑站点)。
   缺口结论：严格全对接需~56个大地标专属事件；务实做法=现有7固定事件挂对应大地标+关键大地标(路段门户/源头/终点/马瑙斯等15-20个)写专属剧情+其余大地标用到达旁白&随机池，实际再写约15-25个即可。待用户定方向。

相关：[[progress-shop-flow]] [[project-overview]] [[team-workflow]] [[story-route-design]]
