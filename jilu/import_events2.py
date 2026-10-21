# -*- coding: utf-8 -*-
"""解析事件2.txt并追加到事件剧本模板.xlsx的事件表"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl
from openpyxl.styles import Font, PatternFill

# 读取事件2.txt
with open('E:/memory/YouXin/事件2.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 解析事件行（跳过标题和空行）
events = []
current_section = None

for line in lines:
    line = line.strip()
    if not line or line.startswith('以下是') or line.startswith('五、') or line.startswith('路段'):
        continue

    # 识别分段标题
    if line.startswith('一、') or line.startswith('二、') or line.startswith('三、') or line.startswith('四、'):
        current_section = line
        continue

    # 跳过表头行
    if line.startswith('事件ID\t'):
        continue

    # 解析事件数据行
    if '\t' in line:
        cols = line.split('\t')
        if len(cols) >= 24 and cols[0].endswith(('_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008')):
            events.append(cols)

print(f"解析到 {len(events)} 个事件\n")

# 打开事件表
wb = openpyxl.load_workbook('E:/memory/YouXin/jilu/事件剧本模板.xlsx')
ws = wb['事件表']

last_row = ws.max_row
print(f"当前事件表最后一行: {last_row}")
print(f"准备追加事件到第 {last_row+1} 行开始...\n")

# 样式
HIGHLIGHT = PatternFill("solid", fgColor="E1F5FE")  # 淡蓝
BOLD = Font(bold=True, color="01579B")

# 追加事件
for i, event_cols in enumerate(events, 1):
    r = last_row + i

    # 前25列（事件表是24列 + 触发类型插入后变25列）
    # 原24列映射到新结构（第8列是触发类型，后面列号+1）
    col_mapping = {
        0: 1,   # 事件ID
        1: 2,   # 事件类型
        2: 3,   # 事件名称
        3: 4,   # 路段
        4: 5,   # 天数范围
        5: 6,   # 触发概率
        6: 7,   # 触发条件
        7: 8,   # 触发类型（新加的）
        8: 9,   # 事件描述
        9: 10,  # 选项1文本
        10: 11, # 选项1效果
        11: 12, # 选项1获得物品
        12: 13, # 选项1消耗物品
        13: 14, # 选项1结果文本
        14: 15, # 选项2文本
        15: 16, # 选项2效果
        16: 17, # 选项2获得物品
        17: 18, # 选项2消耗物品
        18: 19, # 选项2结果文本
        19: 20, # 选项3文本
        20: 21, # 选项3效果
        21: 22, # 选项3获得物品
        22: 23, # 选项3消耗物品
        23: 24, # 选项3结果文本
        24: 25, # 备注
    }

    for src_col, dest_col in col_mapping.items():
        if src_col < len(event_cols):
            val = event_cols[src_col].strip()
            if val and val not in ['', 'None', 'none']:
                ws.cell(row=r, column=dest_col, value=val)

                # 事件ID加粗高亮
                if dest_col == 1:
                    ws.cell(row=r, column=dest_col).font = BOLD
                    ws.cell(row=r, column=dest_col).fill = HIGHLIGHT

    eid = event_cols[0] if len(event_cols) > 0 else ''
    ename = event_cols[2] if len(event_cols) > 2 else ''
    seg = event_cols[3] if len(event_cols) > 3 else ''
    print(f"[{i:2d}] {eid:20s} {ename:20s} ({seg})")

print(f"\n已追加到第 {last_row+1}-{last_row+len(events)} 行")
print(f"事件表现在共 {ws.max_row} 行（含表头）")

wb.save('E:/memory/YouXin/jilu/事件剧本模板.xlsx')
print(f"\n[DONE] 已保存")
