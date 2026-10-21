# DataManager.gd
# 数据管理器 - 单例，加载并提供物品等静态游戏数据
extends Node

var items: Array = []                  # 所有物品(按分类/编号排序)
var items_by_id: Dictionary = {}       # id -> 物品字典

func _ready():
	load_items()
	print("DataManager initialized, items: ", items.size())

# 加载物品数据
func load_items():
	var path = "res://data/items.json"
	if not FileAccess.file_exists(path):
		push_error("items.json not found: " + path)
		return

	var file = FileAccess.open(path, FileAccess.READ)
	if not file:
		push_error("Failed to open items.json")
		return

	var json = JSON.new()
	var err = json.parse(file.get_as_text())
	file.close()

	if err != OK:
		push_error("items.json parse error: " + json.get_error_message())
		return

	items = json.data.get("items", [])
	items_by_id.clear()
	for item in items:
		items_by_id[item["id"]] = item

# 按 id 取物品(找不到返回空字典)
func get_item(id: String) -> Dictionary:
	return items_by_id.get(id, {})

# 取全部物品
func get_all_items() -> Array:
	return items

# 按分类筛选(category: food/water/medical/gear；"all"返回全部)
func get_items_by_category(category: String) -> Array:
	if category == "all":
		return items
	var result: Array = []
	for item in items:
		if item.get("category", "") == category:
			result.append(item)
	return result
