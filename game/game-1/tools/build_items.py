# -*- coding: utf-8 -*-
"""
build_items.py —— 物品数据构建管线
读取 tupian/商店物品图标/物品说明.xlsx 的数值，
结合下面的元数据映射(英文id/英文名/分类/双语描述)，
输出:
  - data/items.json            游戏读取的物品数据
  - assets/images/icons/items/F*.png   256x256 缩略图
  - localization/zh.json, en.json      注入 item.* 名称与描述key
可重复运行(幂等)。修改 xlsx 后重跑即可。
"""
import os, json, io
import openpyxl
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, "..", "..", "tupian", "商店物品图标", "物品说明.xlsx")
SRC_ICONS = os.path.join(ROOT, "..", "..", "tupian", "商店物品图标")
OUT_ICONS = os.path.join(ROOT, "assets", "images", "icons", "items")
OUT_JSON = os.path.join(ROOT, "data", "items.json")
LOC_DIR = os.path.join(ROOT, "localization")
ICON_SIZE = 256

# 分类: food 食物 / water 水 / medical 医疗 / gear 工具装备
# 每项: (item_id, en_name, category, zh_desc, en_desc)
META = {
"F1": ("jerky", "Jerky", "food", "耐储存的高能肉干，需配水食用。", "High-energy preserved meat, drink water with it."),
"F2": ("cassava_flour", "Cassava Flour", "food", "需烹饪的主食，生食有毒。", "Staple that must be cooked; toxic raw."),
"F3": ("compressed_biscuit", "Compressed Biscuit", "food", "即食耐储存口粮。", "Instant, long-lasting ration."),
"F4": ("canned_beans", "Canned Beans", "food", "即食罐头，含汤水但较重。", "Ready-to-eat can with broth, but heavy."),
"F5": ("energy_bar", "Energy Bar", "food", "轻量即食能量补充。", "Light instant energy snack."),
"F6": ("cooking_oil", "Cooking Oil", "food", "烹饪调味，提升食物效果。", "Cooking oil; boosts other food effects."),
"F7": ("sugar", "Sugar", "food", "快速补充能量。", "Quick energy boost."),
"F8": ("instant_coffee", "Instant Coffee", "food", "提神饮品，可能失眠。", "Stimulant drink; may cause insomnia."),
"F9": ("self_heating_meal", "Self-Heating Meal", "food", "即食自加热整餐。", "Instant self-heating full meal."),
"F10": ("water_bottle", "Bottled Water", "water", "即饮干净水。", "Clean drinkable water."),
"F11": ("water_tablet", "Water Purification Tablet", "water", "净化生水，1片1升。", "Purifies raw water, 1 tab per liter."),
"F12": ("water_filter", "Portable Water Filter", "water", "可重复净化生水。", "Reusable water purifier."),
"F13": ("first_aid_kit", "First Aid Kit", "medical", "基础伤口处理。", "Basic wound treatment."),
"F14": ("antibiotics", "Antibiotics", "medical", "广谱抗细菌感染。", "Broad-spectrum antibacterial."),
"F15": ("antimalarial", "Antimalarial", "medical", "治疗与预防疟疾。", "Treats and prevents malaria."),
"F16": ("antivenom", "Snake Antivenom", "medical", "蛇咬急救，立即解毒。", "Snakebite emergency, instant cure."),
"F17": ("antidiarrheal", "Antidiarrheal", "medical", "立即止腹泻。", "Stops diarrhea instantly."),
"F18": ("insect_repellent", "Insect Repellent", "medical", "防蚊虫叮咬。", "Repels insects."),
"F19": ("waterproof_bandage", "Waterproof Bandage", "medical", "伤口包扎防感染。", "Wound dressing, prevents infection."),
"F20": ("vitamins", "Vitamins", "medical", "补充营养防缺乏症。", "Nutrition supplement."),
"F21": ("machete", "Machete", "gear", "开路、狩猎、战斗。", "Clearing path, hunting, combat."),
"F22": ("hiking_boots", "Hiking Boots", "gear", "行军必备鞋具。", "Essential marching footwear."),
"F23": ("tarp", "Tarp", "gear", "搭建庇护所。", "Build a shelter."),
"F24": ("hammock", "Hammock", "gear", "睡眠休息。", "For sleeping and resting."),
"F25": ("sleeping_bag", "Sleeping Bag", "gear", "保暖睡眠。", "Warm sleep gear."),
"F26": ("rope", "Rope", "gear", "攀爬、搭建。", "Climbing and building."),
"F27": ("headlamp", "Headlamp", "gear", "夜间照明。", "Night lighting."),
"F28": ("waterproof_backpack", "Waterproof Backpack", "gear", "储物容器，80L防雨。", "80L waterproof storage."),
"F29": ("trap", "Animal Trap", "gear", "狩猎小型动物。", "Hunts small animals."),
"F30": ("lighter", "Lighter", "gear", "生火。", "Makes fire."),
"F31": ("compass", "Compass", "gear", "导航防迷路。", "Navigation, prevents getting lost."),
}

CAT_ORDER = {"food": 0, "water": 1, "medical": 2, "gear": 3}

def _num(v):
    """单元格转数值；空或非数返回0。"""
    if v is None or str(v).strip() == "":
        return 0
    try:
        return int(v)
    except (ValueError, TypeError):
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0

def _str(v):
    return "" if v is None else str(v).strip()

def read_xlsx():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["Sheet1"]
    # 表头 -> 列号
    head = {}
    for ci in range(1, ws.max_column + 1):
        h = _str(ws.cell(1, ci).value)
        if h:
            head[h] = ci
    rows = {}
    for r in range(2, ws.max_row + 1):
        code = _str(ws.cell(r, head["序号"]).value)
        if not code:
            continue
        def g(col):
            return ws.cell(r, head[col]).value if col in head else None
        rows[code] = {
            "zh_name": _str(g("名称")),
            "price": _num(g("价格(美元)")),
            "weight": _num(g("重量(g)")),
            "uses": _num(g("使用次数")),
            "food": _num(g("饱食")),
            "water": _num(g("水分")),
            "stamina": _num(g("体力")),
            "energy": _num(g("精力")),
            "health": _num(g("健康")),
            "temperature": _num(g("体温")),
            "special": _str(g("特殊效果")),
            "risk": _str(g("负面风险/副作用")),
            "need_cook": _str(g("需烹饪")),
            "shelf_life": _str(g("耐储存")),
            "note": _str(g("备注")),
        }
    return rows

def remove_white_bg(im, threshold=238):
    """从四边对接近白色、与边缘连通的像素泛洪填充为透明。
    只去除与边缘相连的背景白，保留物品内部白色(如绷带/高光)。
    threshold: RGB三通道都>=该值视为白底候选。
    返回处理后的 RGBA 图像。"""
    im = im.convert("RGBA")
    W, H = im.size
    px = im.load()

    def is_white(x, y):
        r, g, b, a = px[x, y]
        return a > 0 and r >= threshold and g >= threshold and b >= threshold

    # 从四边所有白色像素开始 BFS
    from collections import deque
    visited = bytearray(W * H)
    dq = deque()
    for x in range(W):
        for y in (0, H - 1):
            if is_white(x, y) and not visited[y * W + x]:
                visited[y * W + x] = 1
                dq.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if is_white(x, y) and not visited[y * W + x]:
                visited[y * W + x] = 1
                dq.append((x, y))

    while dq:
        x, y = dq.popleft()
        px[x, y] = (255, 255, 255, 0)  # 透明
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and not visited[ny * W + nx]:
                if is_white(nx, ny):
                    visited[ny * W + nx] = 1
                    dq.append((nx, ny))

    # 收边羽化：物品轮廓上残留的偏白像素(抗锯齿过渡)做半透明，消除白边
    # 对每个不透明且邻接透明的像素，按其"接近白的程度"降低alpha
    px2 = im.load()
    edge = []
    for y in range(H):
        for x in range(W):
            r, g, b, a = px2[x, y]
            if a > 0:
                neighbors_transparent = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and px2[nx, ny][3] == 0:
                        neighbors_transparent = True
                        break
                if neighbors_transparent:
                    # 越接近白，越透明(亮度从 threshold..255 映射 alpha 255..0)
                    lum = min(r, g, b)
                    if lum >= threshold - 12:
                        t = (lum - (threshold - 12)) / float(255 - (threshold - 12))
                        new_a = int(a * (1.0 - min(1.0, t)))
                        edge.append((x, y, r, g, b, new_a))
    for x, y, r, g, b, na in edge:
        px2[x, y] = (r, g, b, na)
    return im

def build_thumbnails():
    os.makedirs(OUT_ICONS, exist_ok=True)
    count = 0
    for code in META:
        src = os.path.join(SRC_ICONS, code + ".png")
        if not os.path.exists(src):
            print("  [警告] 缺图标:", src)
            continue
        im = Image.open(src).convert("RGBA")
        # 已带透明通道的(如F30)跳过去白底，避免误伤
        has_alpha = im.getchannel("A").getextrema()[0] < 255
        # 先缩到中间尺寸做去白底(兼顾质量与速度)，再缩到目标尺寸
        work = im.copy()
        work.thumbnail((512, 512), Image.LANCZOS)
        if not has_alpha:
            work = remove_white_bg(work)
        work.thumbnail((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
        # 居中贴到正方形透明画布，保证统一尺寸
        canvas = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
        x = (ICON_SIZE - work.width) // 2
        y = (ICON_SIZE - work.height) // 2
        canvas.paste(work, (x, y), work)
        canvas.save(os.path.join(OUT_ICONS, code + ".png"))
        count += 1
    print("  缩略图:", count, "张 ->", OUT_ICONS)

def build_items_json(rows):
    items = []
    for code, (iid, en_name, cat, zh_desc, en_desc) in META.items():
        row = rows.get(code, {})
        items.append({
            "id": iid,
            "icon_code": code,
            "category": cat,
            "icon": "res://assets/images/icons/items/%s.png" % code,
            "name_key": "item.%s.name" % iid,
            "desc_key": "item.%s.desc" % iid,
            "price": row.get("price", 0),
            "weight": row.get("weight", 0),
            "uses": row.get("uses", 0),
            "effects": {
                "food": row.get("food", 0),
                "water": row.get("water", 0),
                "stamina": row.get("stamina", 0),
                "energy": row.get("energy", 0),
                "health": row.get("health", 0),
                "temperature": row.get("temperature", 0),
            },
            "special": row.get("special", ""),
            "risk": row.get("risk", ""),
            "need_cook": row.get("need_cook", "") in ("是", "是(辅助)"),
        })
    items.sort(key=lambda x: (CAT_ORDER.get(x["category"], 9), x["icon_code"]))
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with io.open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)
    print("  items.json:", len(items), "项 ->", OUT_JSON)
    return items

def inject_localization(rows):
    # 物品名/描述 + 商店/角色创建 UI key
    ui_zh = {
        "ui.character_create.start": "开始旅程",
        "ui.character_create.name_hint": "2-12个字符",
        "ui.character_create.name_invalid": "名字需为2-12个字符",
        "ui.character_create.select_difficulty": "选择难度",
        "ui.shop.title": "村庄补给站",
        "ui.shop.money": "资金",
        "ui.shop.weight": "负重",
        "ui.shop.buy": "购买",
        "ui.shop.owned": "已有",
        "ui.shop.continue": "出发",
        "ui.shop.cant_afford": "资金不足",
        "ui.shop.cat.all": "全部",
        "ui.shop.cat.food": "食物",
        "ui.shop.cat.water": "饮水",
        "ui.shop.cat.medical": "医疗",
        "ui.shop.cat.gear": "工具装备",
    }
    ui_en = {
        "ui.character_create.start": "Begin Journey",
        "ui.character_create.name_hint": "2-12 characters",
        "ui.character_create.name_invalid": "Name must be 2-12 characters",
        "ui.character_create.select_difficulty": "Select Difficulty",
        "ui.shop.title": "Village Supply Post",
        "ui.shop.money": "Funds",
        "ui.shop.weight": "Weight",
        "ui.shop.buy": "Buy",
        "ui.shop.owned": "Owned",
        "ui.shop.continue": "Depart",
        "ui.shop.cant_afford": "Not enough funds",
        "ui.shop.cat.all": "All",
        "ui.shop.cat.food": "Food",
        "ui.shop.cat.water": "Water",
        "ui.shop.cat.medical": "Medical",
        "ui.shop.cat.gear": "Gear",
    }
    for code, (iid, en_name, cat, zh_desc, en_desc) in META.items():
        zh_name = rows.get(code, {}).get("zh_name") or en_name
        ui_zh["item.%s.name" % iid] = zh_name
        ui_zh["item.%s.desc" % iid] = zh_desc
        ui_en["item.%s.name" % iid] = en_name
        ui_en["item.%s.desc" % iid] = en_desc

    for lang, extra in (("zh", ui_zh), ("en", ui_en)):
        path = os.path.join(LOC_DIR, lang + ".json")
        with io.open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.update(extra)
        with io.open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("  本地化注入:", lang, "+%d keys" % len(extra))

def main():
    print("[1/4] 读取 xlsx ...")
    rows = read_xlsx()
    print("  读到", len(rows), "行")
    print("[2/4] 生成缩略图 ...")
    build_thumbnails()
    print("[3/4] 生成 items.json ...")
    build_items_json(rows)
    print("[4/4] 注入本地化 ...")
    inject_localization(rows)
    print("完成。")

if __name__ == "__main__":
    main()
