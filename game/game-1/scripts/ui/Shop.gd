# Shop.gd
# 商店界面：赛博风(深黑+青绿霓虹)，分类筛选 + 物品卡片网格 + 购买
extends Control

var current_category: String = "all"
var card_nodes: Array = []   # [{item, buy_btn, owned_label, ...}]

# ---- 配色(参考案例图:近纯黑底+青翡翠霓虹+白字) ----
const C_BG := Color("05080a")            # 近纯黑背景
const C_PANEL := Color("0c1316")         # 卡面
const C_PANEL_HI := Color("122024")      # 卡面高亮
const C_NEON := Color("00e5c0")          # 主霓虹(青翡翠)
const C_CYAN := Color("1ad6b4")          # 次霓虹(青绿)
const C_TEXT := Color("e6f0ee")          # 主文字(近白)
const C_DIM := Color("5e7872")           # 暗文字
const C_RISK := Color("ff6b6b")          # 副作用红
const C_GOLD := Color("ffd24a")          # 价格金

@onready var title: Label = $Header/Title
@onready var money_label: Label = $Header/Info/MoneyLabel
@onready var weight_label: Label = $Header/Info/WeightLabel
@onready var cat_box: HBoxContainer = $CatBar
@onready var grid: VBoxContainer = $ScrollContainer/Grid
@onready var continue_btn: Button = $ContinueBtn

const CATEGORIES = ["all", "food", "water", "medical", "gear"]

# 状态图标
const STATE_ICONS := {
	"food": "🍗", "water": "💧", "stamina": "🏃",
	"energy": "🧠", "health": "❤️", "temperature": "🌡️"
}

func _ready():
	$ColorRect.color = C_BG
	_style_header()
	_build_category_buttons()
	_style_continue_btn()
	continue_btn.pressed.connect(_on_continue)
	_populate_grid()
	refresh_ui()

# ---- StyleBox 工厂 ----
func _neon_box(bg: Color, border: Color, width: int = 2, radius: int = 6) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(width)
	sb.set_corner_radius_all(radius)
	sb.set_content_margin_all(10)
	return sb

func _style_header():
	title.add_theme_color_override("font_color", C_NEON)
	money_label.add_theme_color_override("font_color", C_GOLD)
	weight_label.add_theme_color_override("font_color", C_CYAN)

func _style_continue_btn():
	continue_btn.add_theme_color_override("font_color", C_BG)
	continue_btn.add_theme_color_override("font_hover_color", C_BG)
	continue_btn.add_theme_stylebox_override("normal", _neon_box(C_NEON, C_NEON, 2, 8))
	continue_btn.add_theme_stylebox_override("hover", _neon_box(C_CYAN, C_CYAN, 2, 8))
	continue_btn.add_theme_stylebox_override("pressed", _neon_box(C_CYAN, C_NEON, 2, 8))

# 占位
func refresh_ui():
	title.text = "▸ " + Translator.t("ui.shop.title")
	continue_btn.text = Translator.t("ui.shop.continue") + " ▸"
	_update_header()
	for btn in cat_box.get_children():
		var cat = btn.get_meta("category")
		btn.text = Translator.t("ui.shop.cat." + cat)

func _update_header():
	money_label.text = "◇ " + Translator.t("ui.shop.money") + " $" + str(GameManager.money)
	weight_label.text = "◈ " + Translator.t("ui.shop.weight") + " %.1fkg" % GameManager.current_weight

# ---- 分类按钮 ----
func _build_category_buttons():
	for cat in CATEGORIES:
		var btn := Button.new()
		btn.toggle_mode = true
		btn.text = Translator.t("ui.shop.cat." + cat)
		btn.set_meta("category", cat)
		btn.add_theme_font_size_override("font_size", 18)
		btn.button_pressed = (cat == "all")
		_style_cat_button(btn)
		btn.pressed.connect(func(): _on_category_selected(cat))
		cat_box.add_child(btn)

func _style_cat_button(btn: Button):
	btn.add_theme_color_override("font_color", C_DIM)
	btn.add_theme_color_override("font_pressed_color", C_BG)
	btn.add_theme_color_override("font_hover_color", C_NEON)
	var normal := _neon_box(C_PANEL, C_DIM.darkened(0.2), 1, 6)
	var pressed := _neon_box(C_NEON, C_NEON, 1, 6)
	var hover := _neon_box(C_PANEL_HI, C_NEON, 1, 6)
	btn.add_theme_stylebox_override("normal", normal)
	btn.add_theme_stylebox_override("hover", hover)
	btn.add_theme_stylebox_override("pressed", pressed)

func _on_category_selected(cat: String):
	current_category = cat
	for btn in cat_box.get_children():
		btn.button_pressed = (btn.get_meta("category") == cat)
	_populate_grid()

# ---- 网格 ----
func _populate_grid():
	for child in grid.get_children():
		child.queue_free()
	card_nodes.clear()
	for item in DataManager.get_items_by_category(current_category):
		grid.add_child(_make_card(item))

# ---- 单个物品行(横向条目，独占一整行) ----
func _make_card(item: Dictionary) -> Control:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(0, 120)
	panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	panel.add_theme_stylebox_override("panel", _neon_box(C_PANEL, C_CYAN.darkened(0.3), 1, 8))

	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 16)
	panel.add_child(row)

	# 左：图标
	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(96, 96)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var tex_path = item.get("icon", "")
	if ResourceLoader.exists(tex_path):
		icon.texture = load(tex_path)
	row.add_child(icon)

	# 中：信息区(名称 + 效果 + 作用 + 副作用，竖排)
	var info := VBoxContainer.new()
	info.add_theme_constant_override("separation", 4)
	info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	row.add_child(info)

	# 名称 + 效果(同一行)
	var titlerow := HBoxContainer.new()
	titlerow.add_theme_constant_override("separation", 16)
	var name_label := Label.new()
	name_label.text = Translator.t(item.get("name_key", ""))
	name_label.add_theme_font_size_override("font_size", 22)
	name_label.add_theme_color_override("font_color", C_TEXT)
	titlerow.add_child(name_label)
	var eff_text := _format_effects(item)
	if eff_text != "":
		var eff := Label.new()
		eff.text = eff_text
		eff.add_theme_font_size_override("font_size", 16)
		eff.add_theme_color_override("font_color", C_NEON)
		eff.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		titlerow.add_child(eff)
	info.add_child(titlerow)

	# 作用说明(special)
	var special = str(item.get("special", "")).strip_edges()
	if special != "":
		var sp := Label.new()
		sp.text = "▹ " + special
		sp.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		sp.add_theme_font_size_override("font_size", 13)
		sp.add_theme_color_override("font_color", C_CYAN)
		info.add_child(sp)

	# 副作用(risk，红字)
	var risk = str(item.get("risk", "")).strip_edges()
	if risk != "":
		var rk := Label.new()
		rk.text = "⚠ " + risk
		rk.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		rk.add_theme_font_size_override("font_size", 13)
		rk.add_theme_color_override("font_color", C_RISK)
		info.add_child(rk)

	# 右：价格 + 已购 + 购买按钮(竖排，固定宽)
	var actions := VBoxContainer.new()
	actions.add_theme_constant_override("separation", 6)
	actions.custom_minimum_size = Vector2(160, 0)
	actions.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	row.add_child(actions)

	var price_label := Label.new()
	price_label.text = "$" + str(item.get("price", 0))
	price_label.add_theme_font_size_override("font_size", 24)
	price_label.add_theme_color_override("font_color", C_GOLD)
	price_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	actions.add_child(price_label)

	var owned_label := Label.new()
	owned_label.add_theme_font_size_override("font_size", 14)
	owned_label.add_theme_color_override("font_color", C_DIM)
	owned_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	actions.add_child(owned_label)

	var buy_btn := Button.new()
	buy_btn.add_theme_font_size_override("font_size", 18)
	var item_id = item.get("id", "")
	buy_btn.pressed.connect(func(): _on_buy(item_id))
	actions.add_child(buy_btn)

	var entry := {"item": item, "owned_label": owned_label, "buy_btn": buy_btn}
	card_nodes.append(entry)
	_update_card(entry)
	return panel

# 效果文本：🍗+30 💧-3 🏃+10
func _format_effects(item: Dictionary) -> String:
	var parts: Array = []
	var eff = item.get("effects", {})
	for key in ["food", "water", "stamina", "energy", "health", "temperature"]:
		var v = int(eff.get(key, 0))
		if v != 0:
			var sign = "+" if v > 0 else ""
			parts.append(STATE_ICONS[key] + sign + str(v))
	return "  ".join(parts)

func _update_card(entry: Dictionary):
	var item = entry["item"]
	var item_id = item.get("id", "")
	var owned = GameManager.get_owned_count(item_id)
	entry["owned_label"].text = Translator.t("ui.shop.owned") + " ×" + str(owned)
	var affordable = GameManager.can_afford(item_id)
	var btn: Button = entry["buy_btn"]
	btn.disabled = not affordable
	if affordable:
		btn.text = "＋ " + Translator.t("ui.shop.buy")
		btn.add_theme_color_override("font_color", C_BG)
		btn.add_theme_color_override("font_hover_color", C_BG)
		btn.add_theme_stylebox_override("normal", _neon_box(C_NEON, C_NEON, 2, 6))
		btn.add_theme_stylebox_override("hover", _neon_box(C_CYAN, C_CYAN, 2, 6))
		btn.add_theme_stylebox_override("pressed", _neon_box(C_CYAN, C_NEON, 2, 6))
	else:
		btn.text = Translator.t("ui.shop.cant_afford")
		btn.add_theme_color_override("font_disabled_color", C_DIM)
		btn.add_theme_stylebox_override("disabled", _neon_box(C_PANEL, C_RISK.darkened(0.3), 1, 6))

func _on_buy(item_id: String):
	if GameManager.buy_item(item_id):
		_update_header()
		for entry in card_nodes:
			_update_card(entry)

func _on_continue():
	print("Departing with inventory: ", GameManager.inventory, " money left: ", GameManager.money)
	get_tree().change_scene_to_file("res://scenes/MainGame.tscn")
