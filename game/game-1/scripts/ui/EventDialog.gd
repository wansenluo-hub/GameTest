extends Control
## EventDialog - 事件对话框
## 全屏显示：配图 + 事件名 + 描述 + 选项；选择后显示结果文本

signal event_finished(event_id: String)

@onready var event_image = $Panel/VBox/EventImage
@onready var name_label = $Panel/VBox/NameLabel
@onready var desc_label = $Panel/VBox/DescLabel
@onready var option_list = $Panel/VBox/OptionList
@onready var result_label = $Panel/VBox/ResultLabel
@onready var continue_btn = $Panel/VBox/ContinueBtn

const C_NEON = Color("#00e5c0")
const C_TEXT = Color("#e6f0ee")
const C_RISK = Color("#ff6b6b")
const C_GOLD = Color("#ffd24a")
const EVENT_IMG_DIR = "res://assets/images/events/"

var _current_event: Dictionary = {}

func _ready():
	continue_btn.pressed.connect(_on_continue)
	visible = false

## 显示事件
func show_event(event: Dictionary):
	_current_event = event

	# 配图（存在才显示）
	var img_path = EVENT_IMG_DIR + str(event.get("id", "")) + ".png"
	if ResourceLoader.exists(img_path):
		event_image.texture = load(img_path)
		event_image.visible = true
	else:
		event_image.visible = false

	name_label.text = str(event.get("name", ""))
	desc_label.text = str(event.get("desc", ""))

	# 隐藏结果区，显示选项区
	result_label.visible = false
	continue_btn.visible = false
	option_list.visible = true

	# 清空旧选项
	for child in option_list.get_children():
		child.queue_free()

	# 生成选项按钮
	var options = event.get("options", [])
	if options.is_empty():
		# 无选项事件（待补剧情或auto），直接给个"继续"
		result_label.visible = true
		result_label.text = "（此事件剧情待补充）"
		continue_btn.visible = true
		option_list.visible = false
	else:
		for i in range(options.size()):
			var opt = options[i]
			var btn = Button.new()
			btn.text = opt.get("text", "选项%d" % (i+1))
			btn.custom_minimum_size = Vector2(0, 48)
			btn.add_theme_font_size_override("font_size", 16)
			btn.pressed.connect(_on_option_selected.bind(i))
			option_list.add_child(btn)

	visible = true
	# 暂停时间
	TimeSystem.stop_clock()
	print("[EventDialog] 显示事件: %s" % event.get("id"))

## 选择了某个选项
func _on_option_selected(index: int):
	var options = _current_event.get("options", [])
	if index >= options.size():
		return
	var opt = options[index]

	# 应用效果
	var changes = []
	var effects = opt.get("effects", {})
	for key in effects:
		var val = effects[key]
		_apply_effect(key, val)
		changes.append("%s%+d" % [key, val])

	# 获得物品
	var gains = opt.get("gain_items", {})
	for item_id in gains:
		var cnt = gains[item_id]
		GameManager.inventory[item_id] = GameManager.get_owned_count(item_id) + cnt
		changes.append("获得%s×%d" % [item_id, cnt])

	# 消耗物品
	var costs = opt.get("cost_items", {})
	for item_id in costs:
		var cnt = costs[item_id]
		var have = GameManager.get_owned_count(item_id)
		GameManager.inventory[item_id] = max(0, have - cnt)
		if GameManager.inventory[item_id] <= 0:
			GameManager.inventory.erase(item_id)
		changes.append("消耗%s×%d" % [item_id, cnt])

	# 显示结果文本
	option_list.visible = false
	result_label.visible = true
	var result = opt.get("result_text", "")
	var change_str = "  [" + ", ".join(changes) + "]" if not changes.is_empty() else ""
	result_label.text = result + change_str
	continue_btn.visible = true

	print("[EventDialog] 选项%d: %s" % [index, ", ".join(changes)])

## 应用单个状态效果
func _apply_effect(key: String, val: int):
	match key:
		"stamina": GameManager.stamina = clamp(GameManager.stamina + val, 0, 100)
		"energy": GameManager.energy = clamp(GameManager.energy + val, 0, 100)
		"food": GameManager.food = clamp(GameManager.food + val, 0, 100)
		"water": GameManager.water = clamp(GameManager.water + val, 0, 100)
		"health": GameManager.health = clamp(GameManager.health + val, 0, 100)
		"temperature": GameManager.temperature = clamp(GameManager.temperature + val, 0, 100)
		"money": GameManager.money = max(0, GameManager.money + val)

## 点击继续，关闭事件
func _on_continue():
	visible = false
	TimeSystem.start_clock()  # 恢复时间
	event_finished.emit(str(_current_event.get("id", "")))
