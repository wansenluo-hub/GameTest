# -*- coding: utf-8 -*-
"""从事件剧本模板.xlsx的站点表生成 stations.json，供游戏加载"""
import io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl

src = 'E:/memory/YouXin/jilu/事件剧本模板_新.xlsx'
if not os.path.exists(src):
    src = 'E:/memory/YouXin/jilu/事件剧本模板.xlsx'
print('读取:', src)

wb = openpyxl.load_workbook(src, read_only=True)
ws = wb['站点表']
rows = list(ws.iter_rows(values_only=True))

stations = []
for r in rows[1:]:
    if not r[0]:
        continue
    sid = str(r[0])
    km = float(r[1]) if r[1] not in (None, '') else 0.0
    seg = str(r[2]) if r[2] else 'andes'
    name_zh = str(r[3]) if r[3] else ''
    name_en = str(r[4]) if r[4] else ''
    stype = str(r[5]) if r[5] else 'waypoint'
    desc = str(r[6]) if r[6] else ''
    event_id = str(r[7]) if r[7] else ''

    if '_event_' in event_id:  # 过滤未写的占位事件ID
        event_id = ''

    stations.append({
        'id': sid, 'km': km, 'segment': seg,
        'name_zh': name_zh, 'name_en': name_en,
        'type': stype, 'desc': desc, 'event_id': event_id,
    })

stations.sort(key=lambda s: s['km'])

out = 'E:/memory/YouXin/game/game-1/data/stations.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'stations': stations}, f, ensure_ascii=False, indent=2)

print(f'[DONE] 已生成 {out}')
print(f'共 {len(stations)} 个站点, 里程 {stations[0]["km"]}-{stations[-1]["km"]} km')
with_event = [s for s in stations if s['event_id']]
print(f'已绑定事件的站点: {len(with_event)} 个')
