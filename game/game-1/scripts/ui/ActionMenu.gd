extends PanelContainer
## ActionMenu - 行动菜单
## 显示可选行动，按上下文过滤

signal action_selected(action_id: String)

@onready var title_label = $VBox/TitleLabel
@onready var action_list = $VBox/ScrollContainer/ActionList

# 行动数据
var actions_data: Array = []

func _ready():
	_load_actions()

## 加载 actions.json
func _load_actions():
	var file = FileAccess.open("res://data/actions.json", FileAccess.READ)
	if file:
		var json = JSON.new()
		var parse_result = json.parse(file.get_as_text())
		if parse_result == OK:
			actions_data = json.data
			print("[ActionMenu] loaded %d actions" % actions_data.size())
		file.close()

## 显示行动菜单（按当前上下文过滤）
func show_menu():
	title_label.text = "选择行动（%s %s）" % [TimeSystem.get_time_name(), TimeSystem.get_weather_name()]

	# 清空旧按钮
	for child in action_list.get_children():
		child.queue_free()

	# 生成可用行动按钮
	var available_actions = _filter_actions()
	for action in available_actions:
		var btn = Button.new()
		btn.text = action["name_zh"]
		btn.custom_minimum_size = Vector2(0, 50)
		# 行军在体力归零时置灰不可点（按钮仍显示）
		if action["id"] == "行军" and GameManager.stamina <= 0:
			btn.disabled = true
			btn.text = action["name_zh"] + "（体力耗尽）"
		else:
			btn.pressed.connect(_on_action_pressed.bind(action["id"]))
		action_list.add_child(btn)

	visible = true
	print("[ActionMenu] showing %d available actions" % available_actions.size())

## 过滤可用行动（样本_2的"出现/过滤条件"列）
func _filter_actions() -> Array:
	var result = []
	for action in actions_data:
		if _check_action_condition(action):
			result.append(action)
	return result

## 检查行动条件
func _check_action_condition(action: Dictionary) -> bool:
	var condition = action.get("condition", "")

	# 行军：任何时候都可用（不强制扎营，不因体力低禁用）

	# 狩猎：陆地站点，雪山/水域不显示（简化：安第斯不显示）
	if action["id"] == "狩猎" and LocationSystem.current_segment == LocationSystem.Segment.ANDES:
		return false

	# 捕鱼：仅河边站点（简化：红区/过渡/巴西可用）
	if action["id"] == "捕鱼" and LocationSystem.current_segment == LocationSystem.Segment.ANDES:
		return false

	# 生火：需wood≥1
	if action["id"] == "生火":
		var wood_count = GameManager.get_owned_count("wood")
		if wood_count < 1:
			return false
		# 雨天成功率×0.4（不禁用，只降低成功率，这里先允许显示）

	# 烹饪：需营火active且有生食材（暂时简化：总是可用）
	# TODO: 检查营火状态和背包生食材

	# 治疗：背包有药品时（暂时简化：总是可用）
	# TODO: 检查背包药品

	# 进食/饮水：背包有食物/水时（暂时简化：总是可用）
	# TODO: 检查背包

	return true

func _on_action_pressed(action_id: String):
	print("[ActionMenu] action selected: %s" % action_id)
	visible = false
	action_selected.emit(action_id)
