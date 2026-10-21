---
name: story-route-design
description: 游戏路线/向导/事件锚点的改编设定与里程数值
metadata:
  type: project
---

用户对真实事件做了改编(2026-06-15确认)：

向导改编：
- 删掉了卢克(Luke)这个角色。
- Cho 从游戏一开始就跟随(真实历史是120天后才加入，游戏里改为开局即在)。
- 村庄可雇佣的向导名称待定(后面再定)。

里程与节奏(已确认)：
- 总里程 9600km(贴合真实9650km)，四路段：安第斯1400km / 红色区域2700km / 过渡地带2700km / 巴西冲刺2800km。
- 行军一次推进 5-8km，乘地形系数(雪山×0.6/红区×0.9/沼泽×0.8/平地×1.0)，全程约1700次行军。
- 时段制：6时段/天每段4h。状态消耗(正常难度,行军1次)：体力-12 饱食-8 水分-10 体温受地形天气影响；被动衰减每时段饱食/水分下降,归零扣健康。
- 进度按距离驱动，进度条显示km/百分比+距下个节点。

事件锚点设计(讨论中)：用户认为固定事件30个太少，要求**起码每~30km一个固定事件**(=约320个节点)，并建议用地名/山名等具名地点作为锚点拆分路段。倾向"站点式"旅程结构。
- 安第斯：Nevado Mismi源头雪山→Colca峡谷→Apurímac河源→Cusco高地→Ene河 (Apurímac→Ene)
- 红色区域：Satipo毒贩区(VRAEM)→Ene-Tambo河谷→Atalaya→Ucayali河→Pucallpa→Contamana→Requena (Ene→Tambo→Ucayali)
- 过渡地带：Requena→Iquitos→秘鲁/巴西边境Santa Rosa→Tabatinga→Benjamin Constant→São Paulo de Olivença→Tefé (Ucayali→Solimões/Amazonas)
- 巴西冲刺：Tefé→Coari→Manaus(里约内格罗汇流)→Parintins→Santarém→Óbidos→Almeirim→Gurupá→Breves→Belém→Marudá(大西洋终点)

站点骨架已生成(2026-06-15)：tools/build_stations.py 生成「站点表」Sheet追加到 jilu/事件剧本模板.xlsx。共321站点(61大地标landmark+260小站点waypoint)，每~30km一站。
- 大地标61个：均真实亚马逊水系地名(中英双名+里程+锚点提示+关联事件ID占位如andes_event_01)，剧情正文和选项由用户在事件表写。安第斯15/红区14/过渡14/巴西18。注:真实地名上限约61个,要凑到用户原想的80个需虚构地名(已与用户说明),用户可后续在事件表把任意小站点升级为大地标。
- 小站点260个：AI按路段词库预填了一句话氛围描述初稿，用户可改。
- 站点表列：站点ID/里程km/路段/地名(中)/地名(英原)/类型/一句话描述锚点/关联事件ID。
- 里程驱动：玩家行军累计km到达站点触发。大地标→对应事件；小站点→显示氛围文字。

下一步：主界面+6行动系统+时间系统+状态系统(事件等剧本)。本轮规划已定行军步长5-8km、状态消耗数值、时段制。代码尚未开始实现。

相关：[[progress-shop-flow]] [[event-script-format]] [[project-overview]]
