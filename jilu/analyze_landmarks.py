# -*- coding: utf-8 -*-
"""分析站点表的61个大地标，挑出最该写专属剧情的~15个高光节点，并对照现有7个固定事件"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl

wb = openpyxl.load_workbook('事件剧本模板.xlsx', read_only=True)
ws_station = wb['站点表']
ws_event = wb['事件表']

# 读站点表
stations = []
for row in list(ws_station.iter_rows(values_only=True))[1:]:
    if not row[0]: continue
    stations.append({
        'id': str(row[0]),
        'km': row[1],
        'segment': str(row[2]),
        'name_zh': str(row[3]) if row[3] else '',
        'name_en': str(row[4]) if row[4] else '',
        'type': str(row[5]),
        'desc': str(row[6]) if row[6] else '',
        'event_id': str(row[7]) if row[7] else ''
    })

landmarks = [s for s in stations if s['type'] == 'landmark']
print(f"共{len(landmarks)}个大地标\n")

# 读事件表，找固定/剧情事件
fixed_events = {}
for row in list(ws_event.iter_rows(values_only=True))[1:]:
    if not row[0]: continue
    eid = str(row[0])
    etype = str(row[1])
    ename = str(row[2])
    # 找固定事件：andes_004/009, season_001, auto_001~004
    if eid in ['andes_004', 'andes_009', 'season_001'] or eid.startswith('auto_'):
        fixed_events[eid] = ename

print("现有7个固定/剧情事件：")
for k,v in fixed_events.items():
    print(f"  {k}: {v}")
print()

# 按路段分组
seg_lm = {'andes':[],'red_zone':[],'transition':[],'brazil':[]}
for lm in landmarks:
    seg_lm[lm['segment']].append(lm)

# 关键节点选择策略
print("="*80)
print("建议补写专属剧情的15个关键大地标清单")
print("="*80)
print()

priority = []

# 路段门户（4个）
priority.append({
    'reason': '【路段门户】安第斯·源头',
    'lm': seg_lm['andes'][0],  # 第一个landmark
    'has_event': 'andes_004',
    'status': '✅已有',
    'note': '源头瀑布（Nevado Mismi），已有andes_004可直接挂'
})

priority.append({
    'reason': '【路段门户】红色区域入口',
    'lm': seg_lm['red_zone'][0],
    'has_event': None,
    'status': '❌需写',
    'note': 'VRAEM毒贩区门户，最危险路段开始（参考样本_5第②个）'
})

priority.append({
    'reason': '【路段门户】过渡地带入口',
    'lm': seg_lm['transition'][0],
    'has_event': None,
    'status': '❌需写',
    'note': '秘鲁/巴西边境，河流变宽，文明渐远'
})

priority.append({
    'reason': '【路段门户】巴西冲刺入口',
    'lm': seg_lm['brazil'][0],
    'has_event': None,
    'status': '❌需写',
    'note': '正式进入巴西亚马逊，Solimões河段开始'
})

# 安第斯高光（再选2个）
priority.append({
    'reason': '【安第斯高光】告别安第斯',
    'lm': seg_lm['andes'][-1],  # 最后一个安第斯landmark
    'has_event': 'andes_009',
    'status': '✅已有',
    'note': '告别安第斯山脉，进入雨林前最后回望'
})

# 找Colca峡谷或Cusco（真实地名中的知名节点）
colca_cusco = [lm for lm in seg_lm['andes'] if 'Colca' in lm['name_en'] or 'Cusco' in lm['name_en']]
if colca_cusco:
    priority.append({
        'reason': '【安第斯高光】科尔卡峡谷/库斯科',
        'lm': colca_cusco[0],
        'has_event': None,
        'status': '❌需写',
        'note': '世界第二深峡谷 或 印加古都，文化地标'
    })
else:
    priority.append({
        'reason': '【安第斯高光】中段关键地标',
        'lm': seg_lm['andes'][len(seg_lm['andes'])//2],
        'has_event': None,
        'status': '❌需写',
        'note': '安第斯中段高海拔节点'
    })

# 红区高光（再选2个）
atalaya = [lm for lm in seg_lm['red_zone'] if 'Atalaya' in lm['name_en']]
pucallpa = [lm for lm in seg_lm['red_zone'] if 'Pucallpa' in lm['name_en']]
if atalaya:
    priority.append({
        'reason': '【红区高光】Atalaya',
        'lm': atalaya[0],
        'has_event': None,
        'status': '❌需写',
        'note': '毒贩区深处的小镇，补给与危险并存'
    })
if pucallpa:
    priority.append({
        'reason': '【红区高光】Pucallpa',
        'lm': pucallpa[0],
        'has_event': None,
        'status': '❌需写',
        'note': 'Ucayali河畔大城，走出VRAEM的第一口气'
    })

# 过渡带高光（选2个）
iquitos = [lm for lm in seg_lm['transition'] if 'Iquitos' in lm['name_en']]
border = [lm for lm in seg_lm['transition'] if 'Santa Rosa' in lm['name_en'] or 'Tabatinga' in lm['name_en']]
if iquitos:
    priority.append({
        'reason': '【过渡带高光】Iquitos',
        'lm': iquitos[0],
        'has_event': None,
        'status': '❌需写',
        'note': '秘鲁雨林最大城市，最后的现代补给点'
    })
if border:
    priority.append({
        'reason': '【过渡带高光】秘鲁/巴西边境',
        'lm': border[0],
        'has_event': None,
        'status': '❌需写',
        'note': 'Santa Rosa三国交界，跨越国界的仪式感'
    })

# 巴西高光（选3-4个）
manaus = [lm for lm in seg_lm['brazil'] if 'Manaus' in lm['name_en']]
santarem = [lm for lm in seg_lm['brazil'] if 'Santarém' in lm['name_en'] or 'Santarem' in lm['name_en']]
belem = [lm for lm in seg_lm['brazil'] if 'Belém' in lm['name_en'] or 'Belem' in lm['name_en']]
maruda = [lm for lm in seg_lm['brazil'] if 'Marudá' in lm['name_en'] or 'Maruda' in lm['name_en']]

if manaus:
    priority.append({
        'reason': '【巴西高光】Manaus马瑙斯',
        'lm': manaus[0],
        'has_event': None,
        'status': '❌需写',
        'note': '黑白河汇流奇观，全程最著名地标（参考样本_5第③个）'
    })
if santarem:
    priority.append({
        'reason': '【巴西高光】Santarém',
        'lm': santarem[0],
        'has_event': None,
        'status': '❌需写',
        'note': 'Tapajós河汇流点，巴西段中期重镇'
    })
if belem:
    priority.append({
        'reason': '【巴西高光】Belém贝伦',
        'lm': belem[0],
        'has_event': None,
        'status': '❌需写',
        'note': '亚马逊河口大城，即将抵达大西洋的前兆'
    })
if maruda:
    priority.append({
        'reason': '【终点】Marudá大西洋终点',
        'lm': maruda[0],
        'has_event': None,
        'status': '❌需写',
        'note': '9600km终点，淡水遇见海水，征途完成'
    })

# 输出清单
print(f"共选出 {len(priority)} 个关键节点\n")
print(f"{'#':<3} {'状态':<8} {'类别':<24} {'站点ID':<20} {'里程':<8} {'地名':<30} {'备注'}")
print("-"*140)
for i, p in enumerate(priority, 1):
    lm = p['lm']
    status = p['status']
    reason = p['reason']
    note = p['note']
    print(f"{i:<3} {status:<8} {reason:<24} {lm['id']:<20} {lm['km']:<8} {lm['name_zh'][:15]:<30} {note[:50]}")

print("\n" + "="*80)
print("统计：")
has = len([p for p in priority if '✅' in p['status']])
need = len([p for p in priority if '❌' in p['status']])
print(f"  已有事件可直接挂: {has} 个")
print(f"  需新写剧情: {need} 个")
print(f"  总计高光节点: {len(priority)} 个")
print()
print("其余 ~{} 个大地标用'到达旁白+随机池'覆盖即可（站点表已有旁白初稿）".format(61-len(priority)))
print("="*80)
