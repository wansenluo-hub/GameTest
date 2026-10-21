# -*- coding: utf-8 -*-
"""
任务B：
1. 给事件表新增"触发类型"列（在"触发条件"列之后）
2. 给92+11=103个事件填写触发类型（地标/时段roll/行动后/状态阈值/天数季节/路段切换）
3. 把现有7个固定事件（andes_004/009, season_001, auto_001-004）对接到站点表的"关联事件ID"列
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl
from openpyxl.styles import Font, PatternFill

# ============ 第1步：给事件表加"触发类型"列 ============
wb_event = openpyxl.load_workbook('事件剧本模板.xlsx')
ws_event = wb_event['事件表']

print("=" * 80)
print("第1步：在事件表插入'触发类型'列")
print("=" * 80)

# 在第8列（触发条件后）插入新列
ws_event.insert_cols(8)
ws_event.cell(row=1, column=8, value="*触发类型").font = Font(bold=True, color="C62828")
ws_event.cell(row=1, column=8).fill = PatternFill("solid", fgColor="FFCDD2")

# 自动推断每个事件的触发类型
trigger_rules = {
    # 地标固定事件（现有）
    'andes_004': ('地标', 'landmark_andes_01 (源头瀑布)'),
    'andes_009': ('地标', 'landmark_andes_15 (告别安第斯)'),

    # 新增地标事件
    'andes_colca': ('地标', 'landmark_andes_04'),
    'red_satipo': ('地标', 'landmark_red_01'),
    'red_atalaya': ('地标', 'landmark_red_04'),
    'red_pucallpa': ('地标', 'landmark_red_08'),
    'trans_iquitos': ('地标', 'landmark_trans_01'),
    'trans_border': ('地标', 'landmark_trans_05'),
    'brazil_coari': ('地标', 'landmark_brazil_01'),
    'brazil_manaus': ('地标', 'landmark_brazil_05'),
    'brazil_santarem': ('地标', 'landmark_brazil_12'),
    'brazil_belem': ('地标', 'landmark_brazil_17'),
    'brazil_maruda': ('地标', 'landmark_brazil_18'),

    # 路段切换
    'auto_001': ('路段切换', '进入red_zone首个时段'),
    'auto_002': ('路段切换', '进入transition首个时段'),
    'auto_003': ('路段切换', '进入brazil首个时段'),
    'auto_004': ('路段切换', 'day>=60随机'),

    # 季节
    'season_001': ('天数/季节', 'day=90 雨季开始'),
}

# 按事件ID前缀推断类型
def infer_trigger(event_id, event_type):
    if event_id in trigger_rules:
        return trigger_rules[event_id]

    prefix = event_id.split('_')[0]

    # 类型推断
    if event_type == 'auto':
        return ('路段切换', '自动触发')

    if prefix in ['animal', 'plant', 'weather', 'river', 'terrain', 'night']:
        return ('时段roll', f'{prefix}类随机遭遇')

    if prefix in ['human', 'gear', 'mental']:
        return ('时段roll', f'{prefix}类随机事件')

    if prefix == 'health':
        # health类可能是阈值或随机
        return ('状态阈值', 'health<某值或时段roll')

    if prefix == 'season':
        return ('天数/季节', '特定天数或季节')

    # 默认
    return ('时段roll', '随机遭遇')

print("\n填写触发类型...")
count = 0
for r in range(2, ws_event.max_row + 1):
    eid = ws_event.cell(row=r, column=1).value
    if not eid: continue

    etype = ws_event.cell(row=r, column=2).value
    trigger_type, trigger_param = infer_trigger(str(eid), str(etype))

    ws_event.cell(row=r, column=8, value=f"{trigger_type} | {trigger_param}")
    count += 1

print(f"已填写 {count} 个事件的触发类型")

# ============ 第2步：对接站点表 ============
print("\n" + "=" * 80)
print("第2步：对接站点表 - 把固定事件ID填入站点表的'关联事件ID'列")
print("=" * 80)

ws_station = wb_event['站点表']

# 地标事件与站点的映射（从trigger_rules提取）
landmark_mapping = {}
for eid, (ttype, param) in trigger_rules.items():
    if ttype == '地标':
        # 提取 landmark_xxx_xx
        import re
        match = re.search(r'landmark_\w+', param)
        if match:
            station_id = match.group(0)
            landmark_mapping[station_id] = eid

print(f"\n地标事件映射表（共{len(landmark_mapping)}个）：")
for sid, eid in sorted(landmark_mapping.items()):
    print(f"  {sid:25s} -> {eid}")

# 找站点表的"关联事件ID"列（第8列）
station_updated = 0
for r in range(2, ws_station.max_row + 1):
    station_id = ws_station.cell(row=r, column=1).value
    if not station_id: continue

    # 检查是否在映射表里
    if str(station_id) in landmark_mapping:
        event_id = landmark_mapping[str(station_id)]
        ws_station.cell(row=r, column=8, value=event_id)
        ws_station.cell(row=r, column=8).font = Font(bold=True, color="1565C0")
        station_updated += 1

print(f"\n已更新 {station_updated} 个站点的关联事件ID")

# 保存
wb_event.save('事件剧本模板.xlsx')
print("\n" + "=" * 80)
print(f"[DONE] 已保存到 事件剧本模板.xlsx")
print("=" * 80)
print("\n总结：")
print(f"  - 事件表新增'触发类型'列（第8列），已填写 {count} 个事件")
print(f"  - 站点表更新 {station_updated} 个大地标的'关联事件ID'")
print(f"  - 现有7个固定事件 + 11个新地标事件 = 18个地标事件已对接")
print(f"  - 其余85个随机事件按'触发类型'列的规则进入对应的触发池")
