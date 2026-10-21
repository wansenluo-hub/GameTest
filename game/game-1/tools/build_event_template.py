# -*- coding: utf-8 -*-
"""生成事件剧本填写模板 事件剧本模板.xlsx"""
import openpyxl, io, json, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "..", "..", "jilu", "事件剧本模板.xlsx")

wb = openpyxl.Workbook()

# 样式
HEAD_FILL = PatternFill("solid", fgColor="1F6F5C")
HEAD_FONT = Font(color="FFFFFF", bold=True, size=11)
REQ_FILL = PatternFill("solid", fgColor="FFE08A")   # 必填列淡黄
EX_FILL = PatternFill("solid", fgColor="EAF4F0")    # 示例行淡绿
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="CCCCCC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(ws, ncol):
    for ci in range(1, ncol + 1):
        c = ws.cell(1, ci)
        c.fill = HEAD_FILL; c.font = HEAD_FONT; c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[1].height = 28
    ws.freeze_panes = "A2"

# ============ Sheet 1: 事件表 ============
ws = wb.active
ws.title = "事件表"

# 列定义: (列名, 宽度, 是否必填, 说明)
COLS = [
    ("事件ID", 14, True, "唯一英文/数字标识，不重复，如 andes_01"),
    ("事件类型", 10, True, "major重大 / minor小事件 / auto自动"),
    ("事件名称", 16, True, "中文标题，如 高原反应"),
    ("路段", 12, True, "andes/red_zone/transition/brazil"),
    ("天数范围", 10, False, "如 1-120，留空=不限"),
    ("触发概率", 8, False, "0-100整数，留空=默认"),
    ("触发条件", 18, False, "可选，如 health<30 或 has_item:antivenom"),
    ("事件描述", 40, True, "正文，玩家看到的情景文字"),
    # 选项1
    ("选项1文本", 18, False, "小事件/自动事件可留空"),
    ("选项1效果", 22, False, "见说明页格式，如 health+10,money-50"),
    ("选项1获得物品", 16, False, "物品id:数量，如 jerky:2"),
    ("选项1消耗物品", 16, False, "物品id:数量，如 antivenom:1"),
    ("选项1结果文本", 28, False, "选择后显示的反馈文字，可留空"),
    # 选项2
    ("选项2文本", 18, False, ""),
    ("选项2效果", 22, False, ""),
    ("选项2获得物品", 16, False, ""),
    ("选项2消耗物品", 16, False, ""),
    ("选项2结果文本", 28, False, ""),
    # 选项3
    ("选项3文本", 18, False, ""),
    ("选项3效果", 22, False, ""),
    ("选项3获得物品", 16, False, ""),
    ("选项3消耗物品", 16, False, ""),
    ("选项3结果文本", 28, False, ""),
    ("备注", 20, False, "给自己/程序的说明，不进游戏"),
]

# 写表头 + 列宽 + 必填列底色
from openpyxl.utils import get_column_letter
for ci, (name, w, req, _desc) in enumerate(COLS, start=1):
    ws.cell(1, ci, name)
    ws.column_dimensions[get_column_letter(ci)].width = w
style_header(ws, len(COLS))
# 必填列表头加标记色(在绿底上用淡黄字提示)
for ci, (name, w, req, _desc) in enumerate(COLS, start=1):
    if req:
        ws.cell(1, ci).value = "*" + name

# 两个示例行
ex1 = ["andes_01","major","高原反应","andes","1-120","30","",
    "你感到头痛欲裂，呼吸急促。卢克脸色苍白，提醒你这是高原反应。",
    "服用抗高反药","health+10","","antimalarial:1","药效缓解了头痛，你感觉好多了。",
    "原地休息2小时","stamina+20,energy+5","","","你靠在岩石上闭眼休息，症状慢慢减轻。",
    "强行下山","health-15,stamina-10","","","你咬牙下撤，但身体付出了代价。",
    "经典高原反应事件，示例"]
ex2 = ["andes_sunrise","minor","壮丽的日出","andes","1-120","","",
    "清晨的阳光照亮雪山顶峰，金色光芒让你暂时忘记疲惫。",
    "继续前进","energy+10","","","",
    "","","","","",
    "","","","","",
    "小事件示例：只有一个选项或自动继续"]

for ri, ex in enumerate([ex1, ex2], start=2):
    for ci, val in enumerate(ex, start=1):
        c = ws.cell(ri, ci, val)
        c.alignment = WRAP; c.border = BORDER; c.fill = EX_FILL

# 预留若干空行带边框
for ri in range(4, 24):
    for ci in range(1, len(COLS) + 1):
        ws.cell(ri, ci).border = BORDER

print("sheet1 ready")

# ============ Sheet 2: 填写说明 ============
ws2 = wb.create_sheet("填写说明")
ws2.column_dimensions["A"].width = 100
GUIDE = [
    ("填写说明", True),
    ("", False),
    ("【基本规则】", True),
    ("1. 每一行 = 一个事件。在「事件表」里填写。", False),
    ("2. 列名带 * 的是必填项(淡黄底)，其余可留空。", False),
    ("3. 中文随便写，英文/数字标识(事件ID、物品id、路段)要照「参考字典」页填，否则程序识别不了。", False),
    ("4. 写完保存，把文件位置告诉AI，AI负责转成游戏数据(JSON)。", False),
    ("", False),
    ("【事件类型】", True),
    ("major  = 重大事件，玩家需要做选择(至少填选项1)", False),
    ("minor  = 小事件，文本提示，通常0-1个选项", False),
    ("auto   = 自动事件，里程碑/季节切换等，无需选择", False),
    ("", False),
    ("【效果列怎么写】", True),
    ("格式: 状态名+数值，多个用英文逗号隔开。正数恢复，负数消耗。", False),
    ("例: health+10,stamina-5,money-50", False),
    ("可用状态名: stamina(体力) energy(精力) food(饱食) water(水分) health(健康) temperature(体温) money(钱)", False),
    ("", False),
    ("【获得/消耗物品列怎么写】", True),
    ("格式: 物品id:数量，多个用英文逗号隔开。", False),
    ("例(获得): jerky:2,water_bottle:1", False),
    ("例(消耗): antivenom:1", False),
    ("物品id 见「参考字典」页，必须一字不差。", False),
    ("", False),
    ("【触发条件列(可选,高级)】", True),
    ("不会写就留空。支持简单条件，AI会帮你完善:", False),
    ("  health<30   健康低于30才触发", False),
    ("  has_item:antivenom   持有抗蛇毒血清才触发", False),
    ("", False),
    ("【结果文本列】", True),
    ("玩家选了这个选项后弹出的反馈文字。可留空。", False),
    ("", False),
    ("【不确定的地方】", True),
    ("数值拿不准就先大概填，或留空+备注说明，AI/后续统一平衡。", False),
    ("先写10-15个核心事件即可让AI搭起系统，不必一次写满。", False),
]
for ri, (text, is_head) in enumerate(GUIDE, start=1):
    c = ws2.cell(ri, 1, text)
    c.alignment = Alignment(wrap_text=True, vertical="center")
    if is_head:
        c.font = Font(bold=True, size=12, color="1F6F5C")

# ============ Sheet 3: 参考字典 ============
ws3 = wb.create_sheet("参考字典")
ws3.column_dimensions["A"].width = 22
ws3.column_dimensions["B"].width = 16
ws3.column_dimensions["C"].width = 22
ws3.column_dimensions["D"].width = 16

ws3.cell(1, 1, "状态名(效果列用)"); ws3.cell(1, 2, "含义")
ws3.cell(1, 3, "路段(路段列用)"); ws3.cell(1, 4, "含义")
states = [("stamina","体力"),("energy","精力"),("food","饱食"),
    ("water","水分"),("health","健康"),("temperature","体温"),("money","钱")]
segs = [("andes","安第斯山区"),("red_zone","红色区域"),
    ("transition","过渡地带"),("brazil","巴西冲刺")]
for i,(k,v) in enumerate(states, start=2):
    ws3.cell(i,1,k); ws3.cell(i,2,v)
for i,(k,v) in enumerate(segs, start=2):
    ws3.cell(i,3,k); ws3.cell(i,4,v)

# 物品id表(从items.json读)
items_path = os.path.join(ROOT, "data", "items.json")
zh_path = os.path.join(ROOT, "localization", "zh.json")
items = json.load(io.open(items_path, encoding="utf-8"))["items"]
zh = json.load(io.open(zh_path, encoding="utf-8"))
start_row = len(states) + 4
ws3.cell(start_row, 1, "物品id(获得/消耗列用)"); ws3.cell(start_row, 2, "中文名")
ws3.cell(start_row, 1).font = Font(bold=True)
ws3.cell(start_row, 2).font = Font(bold=True)
for i, it in enumerate(items, start=start_row + 1):
    ws3.cell(i, 1, it["id"])
    ws3.cell(i, 2, zh.get(it["name_key"], ""))

# 参考字典表头加粗
for ci in (1,2,3,4):
    ws3.cell(1, ci).font = Font(bold=True)
    ws3.cell(1, ci).fill = HEAD_FILL
    ws3.cell(1, ci).font = HEAD_FONT

print("all sheets ready")
wb.save(OUT)
print("saved:", OUT)
