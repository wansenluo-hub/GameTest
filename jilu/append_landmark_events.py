# -*- coding: utf-8 -*-
"""追加12个缺失的地标专属剧情事件到事件表，填必填列+备注，其余留空等用户填写"""
import openpyxl
from openpyxl.styles import Font, PatternFill

PATH = "事件剧本模板.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb['事件表']

# 找当前最后一行
last_row = ws.max_row

# 12个地标事件（按里程顺序）
landmarks = [
    # 事件ID, 事件类型, 事件名称, 路段, 里程km, 站点ID, 备注
    ("andes_colca", "major", "科尔卡峡谷奇观", "andes", 252, "andes_L04",
     "世界第二深峡谷，安第斯段自然高光。可写：俯瞰深渊选择/印加遗迹探索/与condor秃鹫对视。参考样本_5格式"),

    ("red_satipo", "major", "萨蒂波：进入VRAEM", "red_zone", 1400, "red_L01",
     "毒贩区门户，最危险路段开始的转折点。可写：雇向导/改夜行/直接闯。样本_5第②个已有参考"),

    ("red_atalaya", "major", "阿塔拉亚小镇", "red_zone", 1913, "red_L04",
     "毒贩区深处的补给点，危险与希望并存。可写：黑市交易/躲避巡逻/河边露营遭遇"),

    ("red_pucallpa", "major", "普卡尔帕：走出红区", "red_zone", 2804, "red_L08",
     "Ucayali河畔大城，终于走出VRAEM的第一口气。可写：庆祝/补给/听到外界新闻"),

    ("trans_iquitos", "major", "伊基托斯：最后的现代", "transition", 4100, "trans_L01",
     "秘鲁雨林最大城市，最后的现代补给点。可写：奢侈一晚/卖战利品/机场的诱惑（放弃？）"),

    ("trans_border", "major", "三国交界：圣罗莎", "transition", 4937, "trans_L05",
     "秘鲁/巴西/哥伦比亚边境，跨越国界的仪式感。可写：边检/走私者搭讪/纪念拍照"),

    ("brazil_coari", "major", "科阿里：进入巴西", "brazil", 6800, "brazil_L01",
     "正式进入巴西亚马逊，Solimões河段开始。可写：语言障碍/货币兑换/巴西渔民相助"),

    ("brazil_manaus", "major", "马瑙斯：黑白河汇流", "brazil", 7668, "brazil_L05",
     "全程最著名地标，内格罗河墨黑与索里芒斯河浑黄并行不融。样本_5第③个已有参考，你可以改写"),

    ("brazil_santarem", "major", "圣塔伦：塔帕若斯汇流", "brazil", 9012, "brazil_L12",
     "Tapajós河汇流点，巴西段中期重镇。可写：渔市/船只维修/遇到其他探险者"),

    ("brazil_belem", "major", "贝伦：河口之城", "brazil", 9572, "brazil_L17",
     "亚马逊河口大城，即将抵达大西洋的前兆。可写：看到货轮/盐度测试/倒计时开始"),

    ("brazil_maruda", "major", "马鲁达：淡水遇见海水", "brazil", 9600, "brazil_L18",
     "9600km终点，大西洋海滩，征途完成的情感高潮。可写：最后一步/回望/Cho的告别/成就解锁"),
]

# 样式
HIGHLIGHT = PatternFill("solid", fgColor="FFF9C4")  # 淡黄高亮
BOLD = Font(bold=True, color="E65100")

print(f"当前事件表最后一行: {last_row}")
print(f"准备追加 {len(landmarks)} 个地标事件...\n")

# 追加
for i, lm in enumerate(landmarks, 1):
    r = last_row + i
    eid, etype, ename, seg, km, station_id, note = lm

    # 必填列
    ws.cell(row=r, column=1, value=eid).font = BOLD  # *事件ID
    ws.cell(row=r, column=1).fill = HIGHLIGHT
    ws.cell(row=r, column=2, value=etype)  # *事件类型
    ws.cell(row=r, column=3, value=ename).font = Font(bold=True)  # *事件名称
    ws.cell(row=r, column=4, value=seg)  # *路段

    # 天数范围（可选，根据里程估算）
    approx_day = int(km / 6)  # 假设平均6km/天
    ws.cell(row=r, column=5, value=f"{approx_day}-{approx_day+10}")

    # 触发概率：固定事件留空
    ws.cell(row=r, column=6, value="")

    # 触发条件：里程到达
    ws.cell(row=r, column=7, value=f"里程≈{km}km 到达{station_id}")

    # *事件描述：留空等用户填（列8）
    ws.cell(row=r, column=8, value="").fill = PatternFill("solid", fgColor="E8F5E9")  # 淡绿提示待填

    # 选项1-3（列9-23）：全留空
    for col in range(9, 24):
        ws.cell(row=r, column=col, value="").fill = PatternFill("solid", fgColor="E8F5E9")

    # 备注（列24）
    ws.cell(row=r, column=24, value=f"地标专属剧情 | 里程{km}km | {note}")

    print(f"[OK] {i:2d}. {eid:20s} {ename:20s} ({seg}, {km}km) - {station_id}")

print(f"\n已追加到第 {last_row+1}-{last_row+len(landmarks)} 行")
print("绿色底色=待填写内容（事件描述+3组选项）")
print("黄色高亮=新增事件ID")
print("\n格式参考：打开Excel看样本_5（剧本.xlsx）里的3个地标剧情，照着写即可。")

wb.save(PATH)
print(f"\n[DONE] saved to {PATH}")
