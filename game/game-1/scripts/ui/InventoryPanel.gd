extends PanelContainer
## InventoryPanel - 背包面板
## 显示背包物品（图标+中文名+效果），点击使用

signal item_used(item_id: String)

@onready var title_label = $VBox/TitleLabel
@onready var item_grid = $VBox/ScrollContainer/ItemGrid
@onready var close_btn = $VBox/CloseBtn

# 配色（赛博风，与Shop统一）
const C_BG = Color("#0c1316")
const C_PANEL = Color("#122024")
const C_NEON = Color("#00e5c0")
const C_TEXT = Color("#e6f0ee")
const C_DIM = Color("#5e7872")
const C_RISK = Color("#ff6b6b")

# 状态emoji
const STATE_ICONS = {
	"food": "🍗", "water": "💧", "stamina": "🏃",
	"energy": "⚡", "health": "❤", "temperature": "🌡",
}

func _ready():
	close_btn.pressed.connect(_on_close)
	visible = false

## 显示背包
func show_inventory():
	title_label.text = "背包  ( %d 件 · %.1f / %.1f kg )" % [_count_items(), GameManager.current_weight, GameManager.max_weight]

	for child in item_grid.get_children():
		child.queue_free()

	if GameManager.inventory.is_empty():
		var empty = Label.new()
		empty.text = "背包空空如也"
		empty.add_theme_color_override("font_color", C_DIM)
		item_grid.add_child(empty)
	else:
		for item_id in GameManager.inventory:
			var count = GameManager.inventory[item_id]
			if count <= 0:
				continue
			var item = DataManager.get_item(item_id)
			if item.is_empty():
				continue
			_create_item_card(item_id, item, count)

	visible = true

## 创建物品横向卡片（左图标 + 中信息 + 右使用按钮）
func _create_item_card(item_id: String, item: Dictionary, count: int):
	var card = PanelContainer.new()
	card.add_theme_stylebox_override("panel", _make_panel_style())

	var row = HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	card.add_child(row)

	# 左：图标
	var icon = TextureRect.new()
	icon.custom_minimum_size = Vector2(72, 72)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	var icon_path = item.get("icon", "")
	if icon_path != "" and ResourceLoader.exists(icon_path):
		icon.texture = load(icon_path)
	row.add_child(icon)

	# 中：信息区
	var info = VBoxContainer.new()
	info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(info)

	# 名称（中文）× 数量
	var name_label = Label.new()
	var item_name = Translator.t(item.get("name_key", item_id))
	name_label.text = "%s  ×%d" % [item_name, count]
	name_label.add_theme_color_override("font_color", C_TEXT)
	name_label.add_theme_font_size_override("font_size", 18)
	info.add_child(name_label)

	# 效果（emoji + 数值）
	var effects = item.get("effects", {})
	var effect_text = ""
	for key in effects:
		var val = effects[key]
		if val != 0:
			var icon_emoji = STATE_ICONS.get(key, key)
			effect_text += "%s%+d  " % [icon_emoji, val]
	if effect_text != "":
		var effect_label = Label.new()
		effect_label.text = effect_text.strip_edges()
		effect_label.add_theme_color_override("font_color", C_NEON)
		effect_label.add_theme_font_size_override("font_size", 14)
		info.add_child(effect_label)

	# special作用说明（青色）
	var special = item.get("special", "")
	if special != "":
		var special_label = Label.new()
		special_label.text = "▹ " + special
		special_label.add_theme_color_override("font_color", C_NEON)
		special_label.add_theme_font_size_override("font_size", 12)
		special_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		info.add_child(special_label)

	# risk副作用（红色）
	var risk = item.get("risk", "")
	if risk != "":
		var risk_label = Label.new()
		risk_label.text = "⚠ " + risk
		risk_label.add_theme_color_override("font_color", C_RISK)
		risk_label.add_theme_font_size_override("font_size", 12)
		risk_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		info.add_child(risk_label)

	# 右：使用按钮
	var use_btn = Button.new()
	use_btn.text = "使用"
	use_btn.custom_minimum_size = Vector2(80, 60)
	use_btn.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	use_btn.pressed.connect(_on_use_item.bind(item_id, item))
	row.add_child(use_btn)

	item_grid.add_child(card)

## 卡片样式
func _make_panel_style() -> StyleBoxFlat:
	var style = StyleBoxFlat.new()
	style.bg_color = C_PANEL
	style.border_color = C_DIM
	style.set_border_width_all(1)
	style.set_corner_radius_all(6)
	style.set_content_margin_all(10)
	return style

## 使用物品
func _on_use_item(item_id: String, item: Dictionary):
	print("[InventoryPanel] 使用物品: %s" % item_id)

	var effects = item.get("effects", {})
	for key in effects:
		var val = effects[key]
		match key:
			"stamina":
				GameManager.stamina = clamp(GameManager.stamina + val, 0, 100)
			"energy":
				GameManager.energy = clamp(GameManager.energy + val, 0, 100)
			"food":
				GameManager.food = clamp(GameManager.food + val, 0, 100)
			"water":
				GameManager.water = clamp(GameManager.water + val, 0, 100)
			"health":
				GameManager.health = clamp(GameManager.health + val, 0, 100)
			"temperature":
				GameManager.temperature = clamp(GameManager.temperature + val, 0, 100)

	# 扣除物品
	GameManager.inventory[item_id] -= 1
	if GameManager.inventory[item_id] <= 0:
		GameManager.inventory.erase(item_id)

	# 减少负重（weight单位是克）
	var weight = item.get("weight", 0)
	GameManager.current_weight = max(0, GameManager.current_weight - weight / 1000.0)

	item_used.emit(item_id)
	show_inventory()  # 刷新

func _on_close():
	visible = false

func _count_items() -> int:
	var total = 0
	for count in GameManager.inventory.values():
		total += count
	return total
