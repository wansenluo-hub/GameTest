# -*- coding: utf-8 -*-
"""从事件表生成 events.json，解析效果/物品列为结构化数据"""
import io, sys, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl

src = 'E:/memory/YouXin/jilu/事件剧本模板_新.xlsx'
if not os.path.exists(src):
    src = 'E:/memory/YouXin/jilu/事件剧本模板.xlsx'
print('读取:', src)

wb = openpyxl.load_workbook(src, read_only=True)
ws = wb['事件表']
rows = list(ws.iter_rows(values_only=True))

def parse_effects(s):
    """'health+10,stamina-5' -> {'health':10,'stamina':-5}"""
    if not s: return {}
    out = {}
    for part in str(s).split(','):
        part = part.strip()
        m = re.match(r'^([a-z_]+)\s*([+-]\d+)\$', part)
        if m:
            out[m.group(1)] = int(m.group(2))
    return out

def parse_items(s):
    """'jerky:2,antivenom:1' -> {'jerky':2,'antivenom':1}"""
    if not s: return {}
    out = {}
    for part in str(s).split(','):
        part = part.strip()
        m = re.match(r'^([a-z_]+)\s*:\s*(\d+)\$', part)
        if m:
            out[m.group(1)] = int(m.group(2))
    return out

def cell(r, i):
    return str(r[i]).strip() if r[i] not in (None, '') else ''

events = []
for r in rows[1:]:
    if not r[0]:
        continue
    eid = cell(r, 0)

    # 解析3个选项
    options = []
    for base in [9, 14, 19]:  # 选项1/2/3的起始列
        opt_text = cell(r, base)
        if not opt_text:
            continue
        options.append({
            'text': opt_text,
            'effects': parse_effects(cell(r, base+1)),
            'gain_items': parse_items(cell(r, base+2)),
            'cost_items': parse_items(cell(r, base+3)),
            'result_text': cell(r, base+4),
        })

    events.append({
        'id': eid,
        'type': cell(r, 1),          # major/minor/auto
        'name': cell(r, 2),
        'segments': cell(r, 3),       # 路段(可多个逗号)
        'day_range': cell(r, 4),
        'probability': cell(r, 5),
        'condition': cell(r, 6),
        'trigger_type': cell(r, 7),
        'desc': cell(r, 8),
        'options': options,
    })

out = 'E:/memory/YouXin/game/game-1/data/events.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'events': events}, f, ensure_ascii=False, indent=2)

print(f'[DONE] 已生成 {out}')
print(f'共 {len(events)} 个事件')

# 统计有配图的事件
img_dir = 'E:/memory/YouXin/game/game-1/assets/images/events'
imgs = set(f[:-4] for f in os.listdir(img_dir) if f.endswith('.png'))
with_img = [e for e in events if e['id'] in imgs]
print(f'有配图的事件: {len(with_img)} / {len(events)}')

# 选项数统计
opt_counts = {}
for e in events:
    n = len(e['options'])
    opt_counts[n] = opt_counts.get(n, 0) + 1
print('选项数分布:', opt_counts)
