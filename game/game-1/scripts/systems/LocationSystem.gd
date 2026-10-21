extends Node
## LocationSystem - 位置系统 autoload
## 管理：里程/站点/路段/地形

# 路段定义
enum Segment { ANDES, RED_ZONE, TRANSITION, BRAZIL }
const SEGMENT_NAMES = {
	Segment.ANDES: "andes",
	Segment.RED_ZONE: "red_zone",
	Segment.TRANSITION: "transition",
	Segment.BRAZIL: "brazil",
}
const SEGMENT_NAMES_ZH = ["安第斯山区", "红色区域", "过渡地带", "巴西冲刺"]
const SEGMENT_KM = [1400, 2700, 2700, 2800]  # 各路段长度
const SEGMENT_CUMULATIVE_KM = [0, 1400, 4100, 6800, 9600]  # 累计里程

# 地形枚举
enum Terrain { SNOW_MOUNTAIN, RAINFOREST, RIVER_WIDE, SWAMP }

# 当前状态
var total_distance: float = 0.0  # 总里程km
var current_segment: int = Segment.ANDES
var current_terrain: int = Terrain.SNOW_MOUNTAIN
var current_station_id: String = "andes_L01"  # 当前站点（起点）

# 站点数据（从站点表加载）
var stations: Array = []
var stations_by_id: Dictionary = {}

# 信号
signal distance_changed(new_km: float)
signal segment_changed(new_segment: int)
signal station_reached(station: Dictionary)

func _ready():
	_load_stations()
	print("[LocationSystem] ready: km=%.1f segment=%s" % [total_distance, SEGMENT_NAMES_ZH[current_segment]])

## 加载站点表（从 stations.json，共321站点）
func _load_stations():
	var path = "res://data/stations.json"
	if not FileAccess.file_exists(path):
		push_error("[LocationSystem] stations.json not found: " + path)
		return

	var file = FileAccess.open(path, FileAccess.READ)
	var json = JSON.new()
	var err = json.parse(file.get_as_text())
	file.close()

	if err != OK:
		push_error("[LocationSystem] stations.json parse error: " + json.get_error_message())
		return

	stations = json.data.get("stations", [])
	stations_by_id.clear()
	for s in stations:
		stations_by_id[s["id"]] = s

	# 起点设为第一个站点
	if stations.size() > 0:
		current_station_id = stations[0]["id"]

	print("[LocationSystem] loaded %d stations" % stations.size())

## 行军：推进距离
func advance_distance(km: float):
	var old_km = total_distance
	total_distance += km
	distance_changed.emit(total_distance)

	# 检查路段切换
	_check_segment_change()

	# 检查站点到达
	_check_station_reach(old_km, total_distance)

	print("[LocationSystem] advanced %.1f km, total=%.1f km" % [km, total_distance])

## 检查路段切换
func _check_segment_change():
	var new_seg = _get_segment_by_km(total_distance)
	if new_seg != current_segment:
		current_segment = new_seg
		segment_changed.emit(current_segment)
		print("[LocationSystem] !!! 进入新路段: %s" % SEGMENT_NAMES_ZH[current_segment])
		# TODO: 触发 auto_001~003 路段切换事件

## 检查站点到达
func _check_station_reach(old_km: float, new_km: float):
	for s in stations:
		var skm = s["km"]
		if old_km < skm and new_km >= skm:
			current_station_id = s["id"]
			station_reached.emit(s)
			print("[LocationSystem] !!! 到达站点: %s %s (%.1fkm)" % [s["id"], s["name_zh"], skm])
			# TODO: 触发地标事件或显示氛围文字

## 根据里程判断路段
func _get_segment_by_km(km: float) -> int:
	if km < SEGMENT_CUMULATIVE_KM[1]: return Segment.ANDES
	elif km < SEGMENT_CUMULATIVE_KM[2]: return Segment.RED_ZONE
	elif km < SEGMENT_CUMULATIVE_KM[3]: return Segment.TRANSITION
	else: return Segment.BRAZIL

## 获取当前路段名（英文id）
func get_segment_name() -> String:
	return SEGMENT_NAMES[current_segment]

## 获取当前路段名（中文）
func get_segment_name_zh() -> String:
	return SEGMENT_NAMES_ZH[current_segment]

## 获取当前站点
func get_current_station() -> Dictionary:
	return stations_by_id.get(current_station_id, {})

## 距离下一个站点
func get_next_station_distance() -> float:
	for s in stations:
		if s["km"] > total_distance:
			return s["km"] - total_distance
	return 0.0  # 已到终点
