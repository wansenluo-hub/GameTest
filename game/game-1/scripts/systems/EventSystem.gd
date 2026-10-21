extends Node
## EventSystem - 事件系统 autoload
## 加载events.json，按ID取事件 / 按路段随机抽事件

var events: Array = []
var events_by_id: Dictionary = {}

func _ready():
	_load_events()

func _load_events():
	var path = "res://data/events.json"
	if not FileAccess.file_exists(path):
		push_error("[EventSystem] events.json not found")
		return
	var file = FileAccess.open(path, FileAccess.READ)
	var json = JSON.new()
	var err = json.parse(file.get_as_text())
	file.close()
	if err != OK:
		push_error("[EventSystem] parse error: " + json.get_error_message())
		return
	events = json.data.get("events", [])
	for e in events:
		events_by_id[e["id"]] = e
	print("[EventSystem] loaded %d events" % events.size())

## 按ID取事件
func get_event(id: String) -> Dictionary:
	return events_by_id.get(id, {})

## 按当前路段随机抽一个"时段roll"类事件（用于随机遭遇）
func roll_random_event(segment: String) -> Dictionary:
	var pool = []
	for e in events:
		# 只抽时段roll类
		if not str(e.get("trigger_type", "")).begins_with("时段roll"):
			continue
		# 路段匹配（segments含当前路段 或 包含all）
		var segs = str(e.get("segments", ""))
		if segs == "all" or segment in segs:
			# 必须有选项（排除待补剧情）
			if not e.get("options", []).is_empty():
				pool.append(e)
	if pool.is_empty():
		return {}
	return pool[randi() % pool.size()]

## 取所有有配图的事件（测试用）
func get_events_with_image() -> Array:
	var img_dir = "res://assets/images/events/"
	var result = []
	for e in events:
		var path = img_dir + str(e["id"]) + ".png"
		if ResourceLoader.exists(path) and not e.get("options", []).is_empty():
			result.append(e)
	return result
