# -*- coding: utf-8 -*-
"""生成321站点图片清单CSV，供用户照着批量生成图片"""
import io, sys, os, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl

path = '事件剧本模板_新.xlsx' if os.path.exists('事件剧本模板_新.xlsx') else '事件剧本模板.xlsx'
wb = openpyxl.load_workbook(path, read_only=True)
ws = wb['站点表']
rows = list(ws.iter_rows(values_only=True))

# 路段中文名 + 视觉基调（给绘图参考）
SEG_INFO = {
    'andes': ('安第斯山区', '高海拔雪山/冷色调/稀薄空气/裸露岩脊/冰川融水，蓝灰色为主'),
    'red_zone': ('红色区域', '茂密热带雨林/古柯田/河流/危险氛围/雾气，深绿色为主'),
    'transition': ('过渡地带', '宽阔河面/洪泛森林/漂浮村落/湿润，青绿色为主'),
    'brazil': ('巴西冲刺', '亚马逊主河道/宽阔水域/接近海洋/红树林，蓝青色为主'),
}

stations = [r for r in rows[1:] if r[0]]

# 写CSV
out_path = '站点图片清单.csv'
with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['图片文件名', '站点ID', '类型', '路段', '里程km', '地名(中)', '地名(英)', '氛围/锚点描述', '路段视觉基调', '优先级'])

    for r in stations:
        sid = str(r[0])
        km = str(r[1]) if r[1] else '0'
        seg = str(r[2])
        name_zh = str(r[3]) if r[3] else ''
        name_en = str(r[4]) if r[4] else ''
        stype = str(r[5])
        desc = str(r[6]) if r[6] else ''

        seg_zh, seg_visual = SEG_INFO.get(seg, (seg, ''))
        filename = sid + '.png'

        # 优先级：大地标=高(P1)，小站点=普通(P2)
        priority = 'P1-地标' if stype == 'landmark' else 'P2-小站点'

        w.writerow([filename, sid, stype, seg_zh, km, name_zh, name_en, desc, seg_visual, priority])

print(f'[DONE] 已生成 {out_path}')
print(f'共 {len(stations)} 个站点')

# 统计
from collections import Counter
seg_c = Counter(str(r[2]) for r in stations)
type_c = Counter(str(r[5]) for r in stations)
print('\n按路段:')
for seg, cnt in seg_c.items():
    lm = len([r for r in stations if str(r[2])==seg and str(r[5])=='landmark'])
    wp = cnt - lm
    print(f'  {SEG_INFO.get(seg,(seg,))[0]}: {cnt}张 (地标{lm} + 小站点{wp})')
print(f'\n类型: 地标{type_c.get("landmark",0)} + 小站点{type_c.get("waypoint",0)}')
