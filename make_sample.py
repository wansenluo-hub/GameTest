# -*- coding: utf-8 -*-
"""往 剧本.xlsx 追加"样本_"开头的样本案例Sheet（不动原Sheet1）。
对应《行动循环设计.md》的落地样本：L1循环 / L2行动表 / 物品标签 / 战利品表 / 事件触发类型 / L3地标剧情 / 运行走查。
可重跑：先删旧的样本_ Sheet再重建。"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

PATH = "E:/memory/YouXin/剧本.xlsx"
wb = openpyxl.load_workbook(PATH)

# 清掉旧的样本Sheet，幂等
for name in list(wb.sheetnames):
    if name.startswith("样本_"):
        del wb[name]

# ---- 样式 ----
HEAD_FILL = PatternFill("solid", fgColor="0E3B2E")   # 深绿
HEAD_FONT = Font(color="00E5C0", bold=True, size=11)  # 青翡翠
TITLE_FONT = Font(color="0E3B2E", bold=True, size=13)
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="C8D6CE")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def sheet(name, widths):
    ws = wb.create_sheet(name)
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    return ws

def head(ws, row, headers):
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.fill = HEAD_FILL; cell.font = HEAD_FONT
        cell.alignment = WRAP; cell.border = BORDER

def put(ws, r, vals, wrap=True):
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        if wrap: cell.alignment = WRAP
        cell.border = BORDER

print("sheets cleared, building...")

# ============================================================
# 0. 读我（导航页）
# ============================================================
ws = sheet("样本_0_读我", {"A": 14, "B": 90})
ws["A1"] = "行动循环设计 · 样本案例"; ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:B1")
intro = [
 ("是什么", "把《行动循环设计.md》的抽象设计，落成一份可直接照抄的具体样本。看完这几张表，你就知道'剧本只填内容、系统组合分支'到底长什么样。"),
 ("怎么看", "建议顺序：本页 → 样本_6_运行走查（先看效果）→ 样本_2_行动表 → 样本_3_物品标签 → 样本_5_地标剧情。"),
 ("", ""),
 ("样本_1_时段循环", "L1：一天6时段，每时段系统做哪些事（被动衰减→检查事件→弹行动菜单）。纯代码，剧本不参与。"),
 ("样本_2_行动表", "L2核心：10个行动的消耗/产出/选项/条件。这是actions.json的雏形，填表即可，不写代码分支。"),
 ("样本_3_物品标签", "解放分支的关键。给物品加'功能标签'，选项靠标签自动生成。含'打火机vs钻木''芦苇毛当火绒'两个原始疑问的解法。"),
 ("样本_4_战利品表", "L2数值：狩猎/捕鱼/采集 按地形+概率roll出什么。loot_tables雏形。"),
 ("样本_5_地标剧情", "L3：唯一需要灵感的部分。3个真实地标的专属剧情样本（源头瀑布/毒贩区门户/马瑙斯汇流），演示固定事件怎么写。"),
 ("样本_6_运行走查", "把上面的表喂给系统，模拟玩家走2个时段，逐步证明：没有任何一条分支是手写的，全是系统读表组合。"),
 ("样本_7_事件触发类型", "给现有92事件加一列'触发类型'，把85个随机事件接进L1循环的样本。"),
]
r = 3
for k, v in intro:
    ws.cell(row=r, column=1, value=k).font = Font(bold=True, color="0E3B2E")
    ws.cell(row=r, column=1).alignment = WRAP
    ws.cell(row=r, column=2, value=v).alignment = WRAP
    r += 1
for i in range(3, r):
    ws.row_dimensions[i].height = 42

wb.save(PATH)
print("page 0 done")

# ============================================================
# 1. 时段循环 (L1)
# ============================================================
ws = sheet("样本_1_时段循环", {"A":6,"B":10,"C":52,"D":40})
ws["A1"]="L1 旅程循环：一天=6时段×4h，每时段系统按固定流程跑（剧本0参与）"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:D1")
head(ws,3,["步","流程","系统做什么","样本（正常难度数值）"])
rows=[
 ("1","显示","当前位置/时段/天气/状态条；若里程到达站点，显示该站氛围文字","到达waypoint_023→显示'河水浑浊，岸边有脚印'(站点表已有初稿)"),
 ("2","被动衰减","不论玩家做什么，每时段固定扣","饱食-3 水分-4 精力-2 体温向环境温度漂移；任一归0则健康-5"),
 ("3a","固定事件","按km/天数绑定→命中则全屏播放","里程到3.2km→andes_004源头瀑布(见样本_5)"),
 ("3b","随机池roll","按当前路段概率抽85池里的随机事件","红区·黄昏 roll到 human_005毒贩盘查(概率列见样本_7)"),
 ("3c","阈值事件","状态越线触发","health<30→触发'濒死幻觉'；water=0→脱水debuff"),
 ("4","行动菜单","无全屏事件时，按上下文过滤后弹出可选行动","白天河边营地→可选:行军/捕鱼/采集/生火/休息(见样本_2过滤规则)"),
 ("5","结算","玩家选行动→扣消耗→roll产出→可能触发'行动后事件'→推进1时段→回到步1","选'狩猎-用军刀'→体力-10→roll 50%→得meat×1→进入下一时段"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=46
ws["A12"]="昼夜规则：凌晨/清晨/上午/午后/黄昏/夜。夜间行军距离×0.7且健康风险↑；夜间捕鱼可得发光鱼；体温夜间下行更快。"
ws.merge_cells("A12:D12"); ws["A12"].alignment=WRAP; ws.row_dimensions[12].height=30

wb.save(PATH)
print("page 1 done")

# ============================================================
# 2. 行动表 (L2) —— actions.json 雏形
# ============================================================
ws = sheet("样本_2_行动表", {"A":12,"B":6,"C":30,"D":30,"E":48,"F":34})
ws["A1"]="L2 行动定义表：填表即可，选项的'条件'由系统扫背包自动判定，不手写分支"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:F1")
head(ws,3,["行动","时段","消耗","产出/效果","选项（基础选项 + 标签规则）","出现/过滤条件"])
rows=[
 ("行军",1,"体力-12 饱食-8 水分-10 精力-5","前进5-8km×地形系数",
  "①正常行军 ②强行军(规则:体力>40才显示;体力-20但距离+50%,健康-3风险)","体力≤15时禁用"),
 ("狩猎",1,"体力-10 精力-5","成功→meat×1-2，可能+animal_fur；失败→无",
  "①徒手陷阱(基础30%) ②规则:有[工具-狩猎:knife]→'用军刀'+20% ③规则:有[工具-狩猎:bullet]→'开枪'+35%,消耗bullet×1","陆地站点;雪山/水域不显示"),
 ("捕鱼",1,"体力-5 精力-3","成功→fish(夜间→glowing_fish)",
  "①徒手摸鱼(基础25%) ②规则:有[工具-捕鱼:hook]+[诱饵:bait]→'下钩'70%,消耗bait×1","仅河边站点"),
 ("采集",1,"体力-6","按地形概率→fruit/mushroom/wood/野生火绒(见样本_4)",
  "①采集(单选，产出靠loot表) ※mushroom有概率有毒","植被地形;雪山产出极低"),
 ("生火","1~2","体力-4，消耗wood×1","点燃'营火'状态(可烹饪/取暖体温+/夜间安全+)",
  "①钻木取火(基础40%;规则:有[火绒:*]→+30%) ②规则:每个[点火源:*]物品各生成一个'用X生火'~95%快速选项","需wood≥1;雨天成功率×0.4"),
 ("烹饪",1,"需active营火+生食材","生食材→熟食材(熟>生,无health风险)",
  "规则:每个[食材-生:*]物品生成一个'烹饪X'选项","仅当营火active且背包有生食材"),
 ("扎营/休息","1~整夜","—","体力/精力大恢复;有营火则体温+",
  "①短歇(1时段,体力+15 精力+10) ②扎营过夜(到次日清晨,大恢复但里程停滞)","任意时段;夜间推荐"),
 ("治疗",1,"消耗对应药品","health+ / 解除特定debuff",
  "规则:每个[药品:X]物品生成一个治疗选项;或仅当有对应debuff时显示","背包有药品时"),
 ("进食","快捷*","—","选背包食物→饱食+(熟>生,生有health风险)",
  "规则:每个[食材-生/熟:*]或[食物]物品各一个选项","背包有可食物;不占整时段"),
 ("饮水","快捷*","—","水分+",
  "①规则:河边站点→'直接喝河水'(water+大,health风险) ②规则:有[储水]→'喝储备水'安全 ③hot_water温泉水","河边或背包有水"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=58
ws.cell(row=r+1,column=1,value="*进食/饮水设为快捷动作（不占或微占时段），避免操作繁琐。'规则:...'这一句话=系统生成选项的依据，你只写规则不写if-else。")
ws.merge_cells(f"A{r+1}:F{r+1}"); ws.cell(row=r+1,column=1).alignment=WRAP; ws.row_dimensions[r+1].height=34

wb.save(PATH)
print("page 2 done")

# ============================================================
# 3. 物品标签 —— items.json 新增"标签"列 雏形
# ============================================================
ws = sheet("样本_3_物品标签", {"A":16,"B":12,"C":26,"D":30,"E":40})
ws["A1"]="物品功能标签：给现有52物品补一列'标签'。选项靠标签生成，这就是'不写分支'的引擎"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:E1")
head(ws,3,["物品id","中文名","功能标签(可多个,分号隔)","6状态effects(原有)","它解锁/影响哪个选项"])
rows=[
 ("lighter","打火机","点火源","-","生火行动追加'用打火机生火'95%快速选项"),
 ("matches","火柴","点火源:消耗","-","生火追加'用火柴生火'(每次消耗1根)"),
 ("flint","燧石","点火源","-","生火追加'用燧石生火'90%"),
 ("dry_reed","干芦苇毛","火绒","-","钻木取火成功率+30%(你的原始疑问②的解法)"),
 ("phosphor","磷光粉","火绒;夜间照明","-","钻木+30%;夜间事件可用"),
 ("wood","木柴","燃料","-","生火行动的前置(无wood则生火不出现)"),
 ("meat","生肉","食材-生","food+20,health-5","进食生成'吃生肉';烹饪生成'烹饪生肉'"),
 ("cooked_meat","熟肉","食材-熟;食物","food+30,stamina+5","进食生成'吃熟肉'(无health风险)"),
 ("knife","军刀","工具-狩猎","-","狩猎追加'用军刀'+20%"),
 ("bullet","子弹","工具-狩猎:消耗","-","狩猎追加'开枪'+35%(消耗1发)"),
 ("fishing_hook","鱼钩","工具-捕鱼","-","捕鱼追加'下钩'(配鱼饵70%)"),
 ("fishing_bait","鱼饵","诱饵:消耗","-","'下钩'的前置,每次消耗1"),
 ("antivenom","抗蛇毒血清","药品:蛇毒","health+10","治疗生成'注射血清';有蛇毒debuff时高亮"),
 ("painkiller","止痛药","药品:疼痛","health+5","治疗生成'服止痛药'"),
 ("hot_water","温泉水","储水;饮品","water+15,temperature+3","饮水追加'喝温泉水'(安全且暖身)"),
 ("sunglasses","墨镜","装备:防雪盲","-","被动:雪山时段降低雪盲概率(穿戴标签,非主动选项)"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=34
note=("读法：'点火源''火绒''工具-狩猎'这些就是标签。系统生火时只做一件事——扫背包里所有带[点火源]的物品，每个生成一个快速选项；"
      "扫[火绒]决定钻木+30%。打火机vs钻木、芦苇毛当火绒，全是这套规则的自然结果，剧本里一条分支都没写。")
ws.cell(row=r+1,column=1,value=note); ws.merge_cells(f"A{r+1}:E{r+1}")
ws.cell(row=r+1,column=1).alignment=WRAP; ws.row_dimensions[r+1].height=48

wb.save(PATH)
print("page 3 done")

# ============================================================
# 4. 战利品表 (L2数值) —— loot_tables 雏形
# ============================================================
ws = sheet("样本_4_战利品表", {"A":14,"B":16,"C":18,"D":50})
ws["A1"]="L2 概率表：行动'成功'后按地形roll产出。填表即可，系统直接读"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:D1")
head(ws,3,["行动","地形/路段","基础成功率","产出权重表(命中后按权重抽)"])
rows=[
 ("狩猎","安第斯高地","30%","animal_fur 40% / meat×1 35% / meat×2 15% / 空手 10%"),
 ("狩猎","红区雨林","45%","meat×1 40% / meat×2 30% / animal_fur 20% / 受伤(health-5) 10%"),
 ("捕鱼","河流(昼)","25%","fish×1 60% / fish×2 25% / crab_meat 15%"),
 ("捕鱼","河流(夜)","25%","glowing_fish 50% / fish×1 35% / 空 15%"),
 ("采集","雨林植被","70%","fruit 35% / mushroom 25% / wood 20% / dry_reed火绒 12% / cocoa_bean 8%"),
 ("采集","雪山","20%","wood 50% / 空 50%（高海拔几乎无可采）"),
 ("采集","沼泽过渡带","65%","fishing_bait虫饵 30% / fruit 25% / mushroom(毒概率↑) 25% / wood 20%"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=30
ws.cell(row=r+1,column=1,value="加成叠加：样本_2里'用军刀+20%''开枪+35%'是在'基础成功率'上加；mushroom命中后再roll一次是否有毒(如30%毒→食用health-15)。这些都是数值，不是分支。")
ws.merge_cells(f"A{r+1}:D{r+1}"); ws.cell(row=r+1,column=1).alignment=WRAP; ws.row_dimensions[r+1].height=40

wb.save(PATH)
print("page 4 done")

# ============================================================
# 5. 地标剧情 (L3) —— 唯一需要灵感的部分，3个真实地标样本
# ============================================================
ws = sheet("样本_5_地标剧情", {"A":15,"B":42,"C":30,"D":30,"E":30})
ws["A1"]="L3 地标专属剧情：唯一手写的部分。沿用事件表24列格式，下面是3个真实地标的完整样本"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:E1")

def block(ws, r, info):
    """info: dict 描述一个地标事件"""
    ws.cell(row=r,column=1,value=info["title"]).font=Font(bold=True,color="00897B",size=12)
    ws.merge_cells(f"A{r}:E{r}"); ws.row_dimensions[r].height=24
    r+=1
    meta=[("事件ID",info["id"]),("绑定地标",info["anchor"]),("触发类型",info["trigger"]),
          ("事件类型",info["etype"]),("路段",info["seg"])]
    for k,v in meta:
        ws.cell(row=r,column=1,value=k).font=Font(bold=True)
        ws.cell(row=r,column=2,value=v); ws.cell(row=r,column=2).alignment=WRAP
        r+=1
    ws.cell(row=r,column=1,value="事件描述").font=Font(bold=True)
    ws.cell(row=r,column=2,value=info["desc"]); ws.cell(row=r,column=2).alignment=WRAP
    ws.merge_cells(f"B{r}:E{r}"); ws.row_dimensions[r].height=60; r+=1
    head(ws,r,["选项","效果(状态/钱)","获得物品","消耗物品","结果文本"]); r+=1
    for opt in info["options"]:
        put(ws,r,opt); ws.row_dimensions[r].height=46; r+=1
    return r+1

r=3
r=block(ws,r,{
 "title":"① 源头瀑布 — Nevado Mismi 雪山（安第斯·真实亚马逊源头）",
 "id":"andes_004","anchor":"landmark_andes_01 (Nevado Mismi)","trigger":"地标(里程≈3km)",
 "etype":"major","seg":"andes",
 "desc":"你站在海拔5170米的米斯米雪山下。冰川融水从岩缝渗出，汇成一道细瀑——这就是亚马逊河9600公里的起点。Cho摘下手套捧起冰水，没说话。再往前，就没有回头路了。",
 "options":[
   ["庄重地舀一捧水喝下，记住这一刻","精力+10,体温-3","glowing_water:1(纪念·源头水)","","你把源头水装进瓶里。它会陪你到大西洋。整支队伍的士气被点燃了。"],
   ["不耽搁，趁体力充沛立刻出发","体力-5,里程+1km","","","Cho点头跟上。你们沉默地踏上征途，身后雪山渐远。"],
   ["在源头扎营，养足精神再走","到次日清晨,体力+30,精力+20","","wood:1","一夜篝火。清晨醒来，霜花覆盖帐篷，但你们准备好了。"],
 ]})
r=block(ws,r,{
 "title":"② 毒贩区门户 — Satipo / VRAEM（红色区域·真实最危险路段）",
 "id":"red_zone_gate","anchor":"landmark_red_01 (Satipo VRAEM入口)","trigger":"地标+路段切换(auto)",
 "etype":"major","seg":"red_zone",
 "desc":"河岸边竖着褪色的木牌：'VRAEM——前方为管制区'。这里是全球可卡因走私的心脏地带。Cho压低声音：'从现在起，遇到陌生船只，先别靠近。' 远处传来一声枪响，惊起白鹭。",
 "options":[
   ["雇一名熟悉地形的本地向导带路(需$40)","money-40,精力+5","","","向导'Mateo'加入。有他在，毒贩盘查事件的风险显著降低。(后续触发概率↓)"],
   ["昼伏夜出，避开一切人类聚居点","体力-15,水分-10,里程+2km","","","你们改在夜间贴岸潜行。安全，但极度消耗。Cho的眼里布满血丝。"],
   ["大大方方走主航道，赌他们不找麻烦","—","","","河面平静了几小时……直到一艘快艇调转船头朝你们驶来。(强制触发 human_005 毒贩盘查)"],
 ]})
r=block(ws,r,{
 "title":"③ 黑白河汇流 — Manaus 马瑙斯（巴西冲刺·全程地标性奇观）",
 "id":"brazil_manaus","anchor":"landmark_brazil_09 (Manaus汇流)","trigger":"地标(里程≈6900km)",
 "etype":"major","seg":"brazil",
 "desc":"内格罗河的墨黑与索里芒斯河的浑黄在此相遇，两股水流并肩奔流十几公里却不相融，一条清晰的界线劈开整条大河。马瑙斯的灯火在岸边亮起——文明，久违了。你已经走了6900公里。",
 "options":[
   ["靠岸补给，痛快吃一顿热食、补充物资","money-30,饱食+40,精力+25","cooked_meat:2,painkiller:1","","你在码头大排档吃到了三个月来第一顿热饭。Cho笑了，这是出发以来第一次。"],
   ["只远远眺望，不进城，保持节奏","精力+15","","","你选择不被文明的舒适绊住脚步。终点已不远，你要一鼓作气。"],
   ["在城里联系外界，发回一段旅程记录","money-10,精力+10","bible:1(陌生人赠)","","你的影像传了出去。一个素不相识的老妇塞给你一本小圣经，说'愿河带你回家'。"],
 ]})
ws.cell(row=r,column=1,value="说明：以上3个就是'要灵感'的L3内容。全程仅需写约15-20个这样的大地标剧情；其余大地标用'到达旁白+随机池'即可。选项的效果/物品列格式与事件表完全一致，转换脚本直接吃。")
ws.merge_cells(f"A{r}:E{r}"); ws.cell(row=r,column=1).alignment=WRAP; ws.row_dimensions[r].height=44

wb.save(PATH)
print("page 5 done")

# ============================================================
# 6. 运行走查 —— 证明"不写分支"，模拟2个时段
# ============================================================
ws = sheet("样本_6_运行走查", {"A":6,"B":40,"C":56})
ws["A1"]="运行走查：把上面的表喂进系统，模拟玩家走2个时段。右列标注'这步分支从哪来'"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:C1")
head(ws,3,["#","系统/玩家发生了什么","分支从哪来？（关键：没有一条是手写的）"])
rows=[
 ("场景","玩家在红区雨林河边营地，黄昏时段。背包有:wood×2, lighter, dry_reed, knife, meat×1。营火未点。",""),
 ("1","系统执行被动衰减：饱食-3 水分-4 精力-2。water降到18。","样本_1 步2，写死的固定规则。"),
 ("2","系统roll固定/随机事件：里程未到地标→跳过；红区·黄昏按样本_7概率roll→这次没命中。","样本_7 触发类型表 + 概率列。系统读表，没命中就继续。"),
 ("3","系统生成行动菜单。过滤：河边→保留'捕鱼/饮水-直接喝河水'；有wood→显示'生火'；体力55>15→'行军'可用。",
      "样本_2'出现条件'列。系统按当前环境+背包扫一遍，自动决定显示哪些行动。"),
 ("4","玩家点'生火'。系统进入生火选项：扫背包→有lighter[点火源]→生成'用打火机生火95%'；基础'钻木取火40%'；有dry_reed[火绒]→钻木项显示'+30%=70%'。",
      "★这就是你最担心的地方。'打火机vs钻木'不是写好的两条分支——是系统扫到[点火源]和[火绒]标签后，当场拼出来的选项。换个没打火机的玩家，这里就只剩钻木70%。样本_3。"),
 ("5","玩家选'用打火机生火'。系统:消耗wood×1，营火变active，体温+4。推进到'夜'时段。",
      "样本_2生火行的'消耗/产出'。纯数值结算。"),
 ("6","回到步1(夜时段)。被动衰减再来一遍。系统roll事件：夜间→无。生成行动菜单：因营火active且背包有meat[食材-生]→新增'烹饪生肉'；河边夜间→捕鱼变成可得'发光鱼'。",
      "'烹饪'选项的出现条件=样本_2'仅当营火active且有生食材'。'发光鱼'=样本_4捕鱼(夜)的产出表。两个新选项都是系统按新状态重算出来的。"),
 ("7","玩家选'烹饪生肉'→meat×1变cooked_meat×1。再选'吃熟肉'→饱食+30。选'扎营过夜'→到次日清晨，体力+30 精力+20。",
      "全部来自样本_2/3的表。从头到尾，剧本里没有任何一句if。"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=58
concl=("结论：玩家这两个时段里经历的所有'分支'——生火方式、火绒加成、能不能烹饪、夜里钓到什么——"
       "100%是系统读 行动表+物品标签+战利品表 在运行时组合出来的。你要手写的，只有样本_5那种地标剧情。"
       "这就是《行动循环设计》第六节'真正要写死的只剩7项，难写的只有第5项'的实证。")
ws.cell(row=r+1,column=1,value=concl); ws.merge_cells(f"A{r+1}:C{r+1}")
ws.cell(row=r+1,column=1).alignment=WRAP; ws.cell(row=r+1,column=1).font=Font(bold=True,color="0E3B2E")
ws.row_dimensions[r+1].height=60

wb.save(PATH)
print("page 6 done")

# ============================================================
# 7. 事件触发类型 —— 给92事件接进循环
# ============================================================
ws = sheet("样本_7_事件触发类型", {"A":16,"B":16,"C":24,"D":48})
ws["A1"]="给现有92事件加一列'触发类型'，把85个随机事件接进L1循环（import_events.py扩展）"
ws["A1"].font=TITLE_FONT; ws.merge_cells("A1:D1")
head(ws,3,["触发类型","样本事件id","触发参数","系统何时取它"])
rows=[
 ("地标","andes_004 / brazil_manaus","绑定landmark_id","行军里程到达该地标时，全屏播放(见样本_5)"),
 ("路段切换:auto","auto_001~004","进入新路段首个时段","跨路段门户事件，一次性"),
 ("时段roll","human_005毒贩盘查","路段=red_zone, 概率=12%/时段","每个时段步3b按当前路段概率抽"),
 ("时段roll","river_006漩涡","路段=transition/brazil, 概率=8%","同上，水域路段才入池"),
 ("行动后:hunt","forage_003发现芦苇毛","紧随'狩猎/采集'结算, 概率15%","玩家做完该行动后追加roll"),
 ("状态阈值","crisis_002濒死幻觉","health<30","状态越线即触发，优先级最高"),
 ("天数/季节","season_001雨季第一场雨","day>=90","到达条件那天的第一个时段"),
]
r=4
for v in rows: put(ws,r,v); r+=1
for i in range(4,r): ws.row_dimensions[i].height=36
ws.cell(row=r+1,column=1,value="92事件里7个固定(地标/天数/路段切换)直接挂；85个随机按'路段+概率'入'时段roll'池，可在全程复用，不绑死单个站点。加这一列后，系统就知道每个事件'什么时候该出现'。")
ws.merge_cells(f"A{r+1}:D{r+1}"); ws.cell(row=r+1,column=1).alignment=WRAP; ws.row_dimensions[r+1].height=44

# 调整Sheet顺序：样本页排到最前
order=[s for s in wb.sheetnames if s.startswith("样本_")] + [s for s in wb.sheetnames if not s.startswith("样本_")]
wb._sheets.sort(key=lambda s: order.index(s.title))

wb.save(PATH)
print("ALL DONE -> ", wb.sheetnames)
