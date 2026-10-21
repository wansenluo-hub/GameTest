# -*- coding: utf-8 -*-
"""把 新建文本文档.txt 里的92个事件整合进 事件剧本模板.xlsx
- 修正填写错误(金钱填错列、列错位)
- 规整为标准24列
- 提取24个事件专属物品到「事件物品表」Sheet
- 92事件写入「事件表」(覆盖示例)
可重复运行。"""
import io, re, json, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "..", "新建文本文档.txt")
TEMPLATE = os.path.join(ROOT, "..", "..", "jilu", "事件剧本模板.xlsx")

# 标准24列(与事件表一致)
NCOL = 24
# 列索引: 0事件ID 1类型 2名称 3路段 4天数 5概率 6条件 7描述
# 选项1: 8文本 9效果 10获得物品 11消耗物品 12结果文本
# 选项2: 13 14 15 16 17 ; 选项3: 18 19 20 21 22 ; 23备注
OPT_GET = [10, 15, 20]   # 获得物品列
OPT_EFF = [9, 14, 19]    # 对应效果列

def parse_events():
    lines = io.open(SRC, encoding="utf-8").read().split("\n")
    events = []
    for ln in lines:
        if "\t" not in ln: continue
        cells = [c.strip() for c in ln.split("\t")]
        c0 = cells[0]
        if c0 == "事件ID": continue
        if re.match(r'^(andes|animal|plant|weather|health|human|gear|mental|river|night|terrain|season|auto)_\d+$', c0):
            events.append(cells)
    return events

def normalize(e):
    """修正错误并补齐到24列。"""
    e = list(e)
    # andes_009: 25列，删掉错位的空列(倒数第二个空列)
    if len(e) == 25:
        # 末列是备注"路段结束"，倒数第二是多余空列
        if e[-2] == "":
            del e[-2]
    # auto_xxx: 14列(简化表头 ID..选项1结果文本=前13列 + 备注)
    # 映射: 0-12 是 ID..选项1结果文本, 13是备注 -> 放到第23列
    if len(e) == 14:
        note = e[13]
        e = e[:13] + [""] * (NCOL - 14) + [note]
    # 补齐/截断到24列
    if len(e) < NCOL:
        e = e + [""] * (NCOL - len(e))
    elif len(e) > NCOL:
        e = e[:NCOL]
    # 修正: 获得物品列里的 money+X 移到对应效果列
    for gi, ei in zip(OPT_GET, OPT_EFF):
        v = e[gi]
        if v and re.search(r'money[+\-]', v):
            # 把money部分挑出来，其余(真物品)留在原列
            parts = [p.strip() for p in v.split(",") if p.strip()]
            moneys = [p for p in parts if re.match(r'^money[+\-]', p)]
            others = [p for p in parts if not re.match(r'^money[+\-]', p)]
            e[gi] = ",".join(others)
            if moneys:
                eff = e[ei].strip()
                e[ei] = (eff + "," if eff else "") + ",".join(moneys)
    return e

events = [normalize(e) for e in parse_events()]
print("解析+规整事件数:", len(events))
bad = [e[0] for e in events if len(e)!=NCOL]
print("列数异常:", bad if bad else "无，全部24列")

# 24个事件专属物品: id -> (中文名, 分类, 用途说明)
# 分类: food食物/material材料/loot战利品/tool工具/special特殊
EVENT_ITEMS = {
    "meat":          ("生肉",       "food",     "狩猎/动物获得，需烹饪"),
    "cooked_meat":   ("熟肉",       "food",     "烹饪后的肉，可直接食用"),
    "crab_meat":     ("蟹肉",       "food",     "红树林螃蟹获得"),
    "fruit":         ("野果",       "food",     "采集获得，补充维生素"),
    "mushroom":      ("蘑菇",       "food",     "Cho辨认的可食用蘑菇"),
    "cocoa_bean":    ("可可豆",     "food",     "野生可可，提神"),
    "hot_water":     ("温泉水",     "food",     "温泉装瓶，可饮/保暖"),
    "wood":          ("木柴",       "material", "生火/搭建材料"),
    "animal_fur":    ("兽皮",       "material", "狩猎战利品，可卖/保暖"),
    "fishing_bait":  ("鱼饵",       "material", "螺肉等，钓鱼用"),
    "phosphor":      ("磷光粉",     "material", "鬼火沼泽沾染，趣味道具"),
    "sunglasses":    ("墨镜",       "tool",     "防雪盲(安第斯)"),
    "knife":         ("军刀",       "tool",     "德国探险家赠，备用刀具"),
    "bullet":        ("子弹",       "tool",     "枪支弹药，特定事件用"),
    "flare":         ("信号弹",     "tool",     "求救信号"),
    "fishing_hook":  ("鱼钩",       "tool",     "钓鱼工具"),
    "firefly_lantern":("萤火虫灯",  "tool",     "趣味照明"),
    "bible":         ("小圣经",     "special",  "传教士赠，精神慰藉"),
    "glowing_fish":  ("发光鱼",     "loot",     "夜钓奇特鱼类"),
    "glowing_water": ("发光水",     "loot",     "装瓶的发光河水"),
    # 泛指/占位(建议后续细化或并入上面)
    "food":          ("食物",       "food",     "泛指食物(建议事件里改用具体物品)"),
}

def col_letter(i): return get_column_letter(i)

# 样式
HEAD_FILL = PatternFill("solid", fgColor="1F6F5C")
HEAD_FONT = Font(color="FFFFFF", bold=True, size=11)
AUTO_FILL = PatternFill("solid", fgColor="FDEBD0")   # auto事件淡橙
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="CCCCCC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def write_events_sheet(wb):
    ws = wb["事件表"]
    # 清空除表头外的所有行
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for ri, e in enumerate(events, start=2):
        is_auto = (e[1] == "auto")
        for ci in range(1, NCOL + 1):
            c = ws.cell(ri, ci, e[ci - 1])
            c.border = BORDER
            c.alignment = WRAP if ci in (8,13,18,23,24) else CENTER
            if is_auto:
                c.fill = AUTO_FILL
    return len(events)

def write_event_items_sheet(wb):
    name = "事件物品表"
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name, 2)  # 放在站点表后
    headers = ["物品id", "中文名", "分类", "用途说明", "效果(待定)", "可卖价(待定)"]
    widths = [18, 12, 10, 30, 16, 12]
    for ci, (h, w) in enumerate(zip(headers, widths), start=1):
        ws.cell(1, ci, h)
        ws.column_dimensions[col_letter(ci)].width = w
        c = ws.cell(1, ci); c.fill = HEAD_FILL; c.font = HEAD_FONT; c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[1].height = 26
    ws.freeze_panes = "A2"
    ri = 2
    for iid, (zh, cat, use) in EVENT_ITEMS.items():
        for ci, val in enumerate([iid, zh, cat, use, "", ""], start=1):
            c = ws.cell(ri, ci, val)
            c.border = BORDER
            c.alignment = WRAP if ci == 4 else CENTER
        ri += 1
    return len(EVENT_ITEMS)

if __name__ == "__main__":
    wb = openpyxl.load_workbook(TEMPLATE)
    n_ev = write_events_sheet(wb)
    n_it = write_event_items_sheet(wb)
    wb.save(TEMPLATE)
    print("写入事件表:", n_ev, "个事件")
    print("写入事件物品表:", n_it, "个物品")
    print("saved:", TEMPLATE)


