# -*- coding: utf-8 -*-
"""生成站点骨架表，追加到 事件剧本模板.xlsx 的「站点表」Sheet。
80个大地标(真实地名,剧情用户写) + 240个小站点(AI填一句话氛围描述)。
总里程9600km，每~30km一个站点。"""
import openpyxl, os, io
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "..", "..", "jilu", "事件剧本模板.xlsx")

# 样式
HEAD_FILL = PatternFill("solid", fgColor="1F6F5C")
HEAD_FONT = Font(color="FFFFFF", bold=True, size=11)
LM_FILL = PatternFill("solid", fgColor="FFE08A")    # 大地标淡黄
WP_FILL = PatternFill("solid", fgColor="EAF4F0")    # 小站点淡绿
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="CCCCCC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

# 四路段大地标(真实亚马逊水系地名序列)
# 每项: (中文名, 英文/原名, 该路段内大致里程占比0-1, 一句话锚点提示)
SEGMENTS = {
"andes": {"name":"安第斯山区","start_km":0,"length":1400,"prefix":"andes",
    "landmarks":[
        ("米斯米雪山","Nevado Mismi",0.00,"亚马逊源头，旅程起点"),
        ("源头冰湖","Laguna McIntyre",0.05,"第一滴亚马逊之水"),
        ("拉里水源","Lari spring",0.11,"高原融雪汇流处"),
        ("科尔卡峡谷","Colca Canyon",0.18,"世界最深峡谷之一"),
        ("卡瓦纳康德","Cabanaconde",0.25,"峡谷边的梯田村"),
        ("阿普里马克河源","Apurímac source",0.33,"印加人称'会说话的神'"),
        ("查尔万卡","Chalhuanca",0.42,"高原小镇补给"),
        ("阿班凯","Abancay",0.52,"安第斯东麓重镇"),
        ("库斯科高地","Cusco highlands",0.61,"印加古都，重要补给"),
        ("圣安娜峡谷","Santa Ana valley",0.69,"下行进入云雾林"),
        ("基亚班巴","Quillabamba",0.77,"咖啡与古柯之乡"),
        ("乌鲁班巴河汇","Urubamba confluence",0.85,"支流汇入主干"),
        ("埃内河谷","Ene River valley",0.92,"危险区前夜"),
        ("云雾林关口","Cloud forest pass",0.97,"安第斯东坡下降"),
        ("红区门户","Red Zone gateway",1.00,"路段终点，进入红色区域"),
    ]},
"red_zone": {"name":"红色区域","start_km":1400,"length":2700,"prefix":"red",
    "landmarks":[
        ("萨蒂波","Satipo",0.00,"毒贩活动区VRAEM核心"),
        ("埃内-坦博汇流","Ene-Tambo confluence",0.06,"两河交汇成坦博河"),
        ("普埃尔托奥科帕","Puerto Ocopa",0.12,"阿沙宁卡人聚居地"),
        ("阿塔拉亚","Atalaya",0.19,"乌卡亚利河起点重镇"),
        ("塞普阿","Sepahua",0.27,"河岸贸易站，古柯种植区"),
        ("布尔加","Bolognesi",0.35,"丛林深处补给点"),
        ("乌卡亚利河湾","Ucayali bend",0.43,"大河蜿蜒"),
        ("普卡尔帕","Pucallpa",0.52,"红区最大城市，重要补给"),
        ("马斯萨亚","Masisea",0.61,"湖区渔村"),
        ("孔塔马纳","Contamana",0.70,"河港小镇"),
        ("奥里略斯","Orellana",0.78,"以征服者命名"),
        ("雷克纳","Requena",0.86,"塔皮切河口"),
        ("瑙塔","Nauta",0.94,"马拉尼翁与乌卡亚利汇成亚马逊河"),
        ("过渡门户","Transition gateway",1.00,"路段终点，进入过渡地带"),
    ]},
"transition": {"name":"过渡地带","start_km":4100,"length":2700,"prefix":"trans",
    "landmarks":[
        ("伊基托斯","Iquitos",0.00,"世界最大无公路连接城市"),
        ("纳波河口","Napo mouth",0.08,"支流汇入"),
        ("印第安纳","Indiana",0.15,"河岸传教镇"),
        ("佩巴斯","Pebas",0.23,"陶艺小镇"),
        ("圣罗莎","Santa Rosa",0.31,"秘鲁边境哨所"),
        ("三国交界","Tabatinga/Leticia",0.38,"秘鲁-哥伦比亚-巴西三国点"),
        ("本杰明康斯坦特","Benjamin Constant",0.45,"进入巴西"),
        ("圣安东尼奥","Santo Antônio do Içá",0.54,"伊萨河口"),
        ("托南廷斯","Tonantins",0.62,"河畔渔镇"),
        ("圣保罗德奥利文萨","São Paulo de Olivença",0.70,"索利蒙伊斯河畔"),
        ("茹塔伊河口","Jutaí mouth",0.79,"黑水支流"),
        ("丰特博阿","Fonte Boa",0.88,"渔业小镇"),
        ("特费","Tefé",0.95,"巴西冲刺前最后大补给"),
        ("巴西冲刺门户","Brazil sprint gateway",1.00,"路段终点，进入巴西冲刺"),
    ]},
"brazil": {"name":"巴西冲刺","start_km":6800,"length":2800,"prefix":"brazil",
    "landmarks":[
        ("科阿里","Coari",0.00,"石油重镇"),
        ("科达雅斯","Codajás",0.10,"巴西坚果之乡"),
        ("阿纳马","Anamã",0.17,"低地泛滥区小镇"),
        ("曼纳卡普鲁","Manacapuru",0.24,"接近大都市"),
        ("马瑙斯","Manaus",0.31,"黑白两河交汇，亚马逊心脏"),
        ("河水交汇奇观","Meeting of Waters",0.34,"黑水与黄水不混"),
        ("伊塔夸蒂亚拉","Itacoatiara",0.43,"港口城市"),
        ("乌鲁卡拉","Urucará",0.51,"河岸小镇"),
        ("帕林廷斯","Parintins",0.58,"牛节之城"),
        ("茹鲁蒂","Juruti",0.65,"铝土矿区"),
        ("奥比多斯","Óbidos",0.72,"亚马逊最窄最深处"),
        ("圣塔伦","Santarém",0.79,"塔帕若斯河汇流"),
        ("蒙蒂阿莱格里","Monte Alegre",0.85,"史前岩画之地"),
        ("阿尔梅林","Almeirim",0.90,"高原台地"),
        ("古鲁帕","Gurupá",0.94,"进入河口三角洲"),
        ("布雷维斯","Breves",0.97,"马拉若岛迷宫水道"),
        ("贝伦","Belém",0.99,"亚马逊门户大城"),
        ("马鲁达海滩","Marudá beach",1.00,"大西洋！旅程终点"),
    ]},
}

print("data defined")

# 各路段小站点氛围描述词库(AI初稿，用户可改)
AMBIENCE = {
"andes": [
    "寒风掠过裸露的岩脊，呼吸在稀薄空气里变得急促。",
    "一片高山苔原延伸到视野尽头，远处雪峰泛着冷光。",
    "脚下的碎石坡很滑，每一步都要试探着落脚。",
    "一群羊驼警觉地抬头，又低下去继续啃食枯草。",
    "云在山谷里翻涌，太阳时隐时现。",
    "你越过一道冰冷的溪流，水来自融化的雪。",
    "高原的夜来得很快，气温骤降。",
    "一座废弃的石屋立在垭口，不知是谁留下的。",
],
"red_zone": [
    "茂密的灌木挡住去路，你挥刀开路，汗水浸透衣背。",
    "远处传来引擎声，你警觉地伏低身子等它远去。",
    "湿热的空气里蚊虫成群，叮咬让人难以忍受。",
    "河岸泥泞，每一步都陷进淤泥里。",
    "一处被遗弃的营地，灰烬还没完全冷却。",
    "藤蔓缠绕的树冠遮天蔽日，正午也像黄昏。",
    "你听到河对岸有人声，分不清是友是敌。",
    "一条小船拴在岸边，主人却不见踪影。",
],
"transition": [
    "河面宽得望不到对岸，独木舟在浪里起伏。",
    "雨季的洪水淹没了岸边的小路，你只能涉水前行。",
    "一群粉红河豚跃出水面，转瞬又消失。",
    "沼泽散发着腐殖质的气味，落脚处越来越少。",
    "边境的哨所空无一人，铁皮屋顶在烈日下发烫。",
    "渔民晾晒的渔网挂满了岸边的木桩。",
    "暴雨说来就来，瞬间打湿一切。",
    "一座浮在水上的村庄，房屋都架在木桩上。",
],
"brazil": [
    "大河如海，浑黄的水一直流向天际。",
    "巨大的货轮鸣笛驶过，掀起的浪差点打翻独木舟。",
    "雨林边缘的城镇灯火渐密，文明的气息越来越近。",
    "潮汐开始影响水位，你能闻到一丝海的咸味。",
    "成片的浮萍随波荡漾，白鹭立在其间。",
    "河口的水道像迷宫，一不小心就会迷失方向。",
    "岸边孩子们朝你挥手，喊着听不懂的葡萄牙语。",
    "夕阳把整条大河染成金红色，终点不远了。",
]
}

STATION_GAP = 30  # 每~30km一个站点

def build_stations():
    rows = []  # 每行: [站点ID, 里程km, 路段, 地名中, 地名英, 类型, 一句话描述, 关联事件ID]
    for seg_key, seg in SEGMENTS.items():
        base = seg["start_km"]
        length = seg["length"]
        prefix = seg["prefix"]
        lms = seg["landmarks"]
        amb = AMBIENCE[seg_key]
        amb_i = 0
        counter = 0
        # 大地标按里程排序(占比*length+base)
        lm_points = [(base + int(p * length), zh, en, hint) for (zh, en, p, hint) in lms]
        # 在相邻大地标之间插入小站点
        for idx in range(len(lm_points)):
            km, zh, en, hint = lm_points[idx]
            counter += 1
            sid = "%s_L%02d" % (prefix, idx + 1)
            ev_id = "%s_event_%02d" % (prefix, idx + 1)  # 大地标关联事件ID占位
            rows.append([sid, km, seg_key, zh, en, "landmark", "★大地标：" + hint, ev_id])
            # 到下一个大地标之间插小站点
            if idx + 1 < len(lm_points):
                next_km = lm_points[idx + 1][0]
                gap = next_km - km
                n_way = max(0, int(round(gap / float(STATION_GAP))) - 1)
                for w in range(1, n_way + 1):
                    wkm = km + int(gap * w / (n_way + 1))
                    counter += 1
                    wsid = "%s_w%03d" % (prefix, counter)
                    desc = amb[amb_i % len(amb)]
                    amb_i += 1
                    rows.append([wsid, wkm, seg_key, "", "", "waypoint", desc, ""])
    return rows

def write_sheet(rows):
    wb = openpyxl.load_workbook(TEMPLATE)
    if "站点表" in wb.sheetnames:
        del wb["站点表"]
    ws = wb.create_sheet("站点表", 1)  # 放在事件表后面
    headers = ["站点ID","里程km","路段","地名(中)","地名(英/原)","类型","一句话描述/锚点","关联事件ID"]
    widths = [14,9,12,18,20,12,46,16]
    for ci,(h,w) in enumerate(zip(headers,widths), start=1):
        ws.cell(1,ci,h)
        ws.column_dimensions[get_column_letter(ci)].width = w
        c = ws.cell(1,ci); c.fill=HEAD_FILL; c.font=HEAD_FONT; c.alignment=CENTER; c.border=BORDER
    ws.row_dimensions[1].height = 28
    ws.freeze_panes = "A2"
    for ri, row in enumerate(rows, start=2):
        is_lm = (row[5] == "landmark")
        for ci, val in enumerate(row, start=1):
            c = ws.cell(ri, ci, val)
            c.border = BORDER
            c.alignment = WRAP if ci in (7,) else CENTER
            c.fill = LM_FILL if is_lm else WP_FILL
    wb.save(TEMPLATE)
    return ws.max_row

rows = build_stations()
# 统计(不依赖写文件)
def _stats(rows):
    lm = sum(1 for r in rows if r[5]=="landmark")
    wp = sum(1 for r in rows if r[5]=="waypoint")
    print("站点骨架: 总%d行 (大地标%d + 小站点%d)" % (len(rows), lm, wp))
    for seg_key, seg in SEGMENTS.items():
        cnt = sum(1 for r in rows if r[2]==seg_key)
        print("  %s: %d站点" % (seg["name"], cnt))

if __name__ == "__main__":
    _stats(rows)
    n = write_sheet(rows)
    print("saved:", TEMPLATE)
