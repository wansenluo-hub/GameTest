# -*- coding: utf-8 -*-
"""从剧本.xlsx的样本_2_行动表转换生成 actions.json"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl
import json

wb = openpyxl.load_workbook('E:/memory/YouXin/剧本.xlsx', read_only=True)
ws = wb['样本_2_行动表']

rows = list(ws.iter_rows(values_only=True))
print("样本_2_行动表列名:", rows[2])
print()

actions = []
for r in rows[3:13]:  # 10个行动（第4-13行）
    if not r[0]: continue

    action_name = str(r[0])

    # 跳过治疗/进食/饮水（改为背包物品直接使用）
    if action_name in ["治疗", "进食", "饮水"]:
        print(f"[SKIP] {action_name} - 改为背包物品使用")
        continue

    # 处理"扎营/休息"→拆成两个
    if action_name == "扎营/休息":
        # 添加"短歇"
        actions.append({
            "id": "rest",
            "name_zh": "短歇",
            "name_en": "rest",
            "time_cost": 1,
            "cost": "",
            "output": "体力+15 精力+10",
            "options_raw": "短歇(1时段,体力+15 精力+10)",
            "condition": "任意时段",
        })
        # 添加"扎营过夜"
        actions.append({
            "id": "camp",
            "name_zh": "扎营过夜",
            "name_en": "camp",
            "time_cost": 6,  # 到次日清晨
            "cost": "",
            "output": "体力+40 精力+30，到次日清晨",
            "options_raw": "扎营过夜(到次日清晨,大恢复但里程停滞)",
            "condition": "任意时段;夜间推荐",
        })
        print(f"[SPLIT] {action_name} → rest + camp")
        continue

    action = {
        "id": action_name.replace('/', '_').replace(' ', '_').lower(),
        "name_zh": action_name,
        "name_en": action_name,
        "time_cost": int(r[1]) if isinstance(r[1], (int, float)) else 1,
        "cost": str(r[2]) if r[2] else "",
        "output": str(r[3]) if r[3] else "",
        "options_raw": str(r[4]) if r[4] else "",
        "condition": str(r[5]) if r[5] else "",
    }

    actions.append(action)
    print(f"[{len(actions)}] {action['id']:15s} {action['name_zh']:12s} 时段={action['time_cost']} 条件={action['condition'][:30]}")

output_path = 'E:/memory/YouXin/game/game-1/data/actions.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(actions, f, ensure_ascii=False, indent=2)

print(f"\n[DONE] 已生成 {output_path}")
print(f"共 {len(actions)} 个行动")
