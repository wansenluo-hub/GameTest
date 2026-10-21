# -*- coding: utf-8 -*-
"""修正版：用站点表实际的站点ID格式对接事件"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl
from openpyxl.styles import Font

wb = openpyxl.load_workbook('事件剧本模板.xlsx')
ws_station = wb['站点表']

# 地标事件与站点的实际映射（用真实站点ID）
landmark_mapping = {
    # 现有固定事件
    'andes_L01': 'andes_004',      # 源头瀑布
    'andes_L15': 'andes_009',      # 告别安第斯

    # 新增地标事件
    'andes_L04': 'andes_colca',    # 科尔卡峡谷
    'red_L01': 'red_satipo',       # 萨蒂波
    'red_L04': 'red_atalaya',      # 阿塔拉亚
    'red_L08': 'red_pucallpa',     # 普卡尔帕
    'trans_L01': 'trans_iquitos',  # 伊基托斯
    'trans_L05': 'trans_border',   # 圣罗莎边境
    'brazil_L01': 'brazil_coari',  # 科阿里
    'brazil_L05': 'brazil_manaus', # 马瑙斯
    'brazil_L12': 'brazil_santarem', # 圣塔伦
    'brazil_L17': 'brazil_belem',  # 贝伦
    'brazil_L18': 'brazil_maruda', # 马鲁达终点
}

print("对接站点表的'关联事件ID'列（第8列）\n")
print(f"{'站点ID':<15} {'原占位符':<20} -> {'新事件ID':<20} {'地名':<20}")
print("-" * 80)

updated = 0
for r in range(2, ws_station.max_row + 1):
    station_id = ws_station.cell(row=r, column=1).value
    if not station_id: continue

    sid = str(station_id)
    if sid in landmark_mapping:
        old_val = ws_station.cell(row=r, column=8).value
        new_event_id = landmark_mapping[sid]
        ws_station.cell(row=r, column=8, value=new_event_id)
        ws_station.cell(row=r, column=8).font = Font(bold=True, color="1565C0")

        name_zh = ws_station.cell(row=r, column=4).value
        print(f"{sid:<15} {str(old_val):<20} -> {new_event_id:<20} {name_zh}")
        updated += 1

wb.save('事件剧本模板.xlsx')
print(f"\n[DONE] 已更新 {updated} 个大地标的关联事件ID")
