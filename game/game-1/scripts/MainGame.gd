extends Control
## MainGame - 主游戏场景
## 实时时钟模型：时间持续流逝（挂机也走），天色平滑渐变
## 行动 = 快进时间 + 结算效果；被动衰减按小时触发

@onready var status_panel = $StatusPanel
@onready var action_menu = $ActionMenu
@onready var inventory_panel = $InventoryPanel
@onready var inventory_btn = $InventoryBtn
@onready var background = $Background  # TextureRect
@onready var day_night_overlay = $DayNightOverlay
@onready var rain_particles = $RainParticles
@onready var action_btn = $ActionBtn
@onready var event_test_btn = $EventTestBtn
@onready var event_dialog = $EventDialog

const C_BG = Color("#05080a")
const C_NEON = Color("#00e5c0")
const C_TEXT = Color("#e0e0e0")

# 行进图目录（按"路段_序号"命名，如 andes_001.png）
const MARCH_IMG_DIR = "res://assets/images/march/"

# 各路段已有的行进图数量（启动时扫描）
var _march_img_count: Dictionary = {}   # segment_name -> 图片张数
# 各路段的行军计数（走了第几次）
var _march_index: Dictionary = {}       # segment_name -> 已行军次数

var _current_bg_key: String = ""

func _ready():
	action_menu.action_selected.connect(_on_action_selected)
	inventory_panel.item_used.connect(_on_item_used)
	inventory_btn.pressed.connect(_on_inventory_btn_pressed)
	action_btn.pressed.connect(_on_action_btn_pressed)
	event_test_btn.pressed.connect(_on_event_test_pressed)
	event_dialog.event_finished.connect(_on_event_finished)

	# 时间系统信号
	TimeSystem.hour_passed.connect(_on_hour_passed)
	TimeSystem.weather_changed.connect(_update_weather_effects)
	LocationSystem.segment_changed.connect(_on_segment_changed)
	LocationSystem.station_reached.connect(_on_station_reached)

	_setup_visuals()

	# 启动实时时钟（时间开始流逝）
	TimeSystem.start_clock()

## 每帧：天色随时间平滑渐变
func _process(_delta):
	_update_day_night_smooth()

## 处理输入（快捷键）
func _input(event: InputEvent):
	# 事件对话框打开时不响应其他快捷键
	if event_dialog.visible:
		return
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_I:
			if inventory_panel.visible:
				inventory_panel.visible = false
			else:
				inventory_panel.show_inventory()
		elif event.keycode == KEY_SPACE:
			# 空格打开行动菜单
			_on_action_btn_pressed()
		elif event.keycode == KEY_E:
			# E 触发随机事件（测试）
			_on_event_test_pressed()

## 测试：触发一个随机事件
func _on_event_test_pressed():
	var seg = LocationSystem.get_segment_name()
	var ev = EventSystem.roll_random_event(seg)
	if ev.is_empty():
		# 当前路段没有匹配的随机事件，从所有有配图的里随便挑一个
		var pool = EventSystem.get_events_with_image()
		if not pool.is_empty():
			ev = pool[randi() % pool.size()]
	if not ev.is_empty():
		event_dialog.show_event(ev)
	else:
		print("[MainGame] 没有可触发的事件")

## 事件结束
func _on_event_finished(_event_id: String):
	status_panel.refresh_status()
	print("[MainGame] 事件结束: %s" % _event_id)

## 初始化视觉
func _setup_visuals():
	_scan_march_images()
	_show_march_image()  # 显示当前路段第一张行进图
	day_night_overlay.color = Color(0, 0, 0, 0)
	rain_particles.emitting = false

## 启动时扫描各路段已有多少张行进图
func _scan_march_images():
	var segs = ["andes", "red_zone", "transition", "brazil"]
	for seg in segs:
		var count = 0
		var n = 1
		# 连续编号探测：andes_001, andes_002... 直到断号
		while true:
			var path = MARCH_IMG_DIR + "%s_%03d.png" % [seg, n]
			if ResourceLoader.exists(path):
				count = n
				n += 1
			else:
				break
		_march_img_count[seg] = count
		_march_index[seg] = 0
		print("[MainGame] 路段 %s 行进图: %d 张" % [seg, count])

## 显示当前路段、当前行军计数对应的行进图（循环复用）
func _show_march_image():
	var seg = LocationSystem.get_segment_name()
	var total = _march_img_count.get(seg, 0)
	if total <= 0:
		# 该路段一张图都没有，保持空（或可放占位）
		return
	var idx = _march_index.get(seg, 0)
	# 循环复用：第idx次行军 -> 第 (idx mod total)+1 张图
	var pic_num = (idx % total) + 1
	var path = MARCH_IMG_DIR + "%s_%03d.png" % [seg, pic_num]
	var key = "march:%s_%d" % [seg, pic_num]
	if key == _current_bg_key:
		return
	if ResourceLoader.exists(path):
		background.texture = load(path)
		_current_bg_key = key

## 站点到达：仅打印氛围/地名，触发地标事件（不再换背景，背景由行军驱动）
func _on_station_reached(station: Dictionary):
	var name_zh = str(station.get("name_zh", ""))
	var desc = str(station.get("desc", ""))
	var event_id = str(station.get("event_id", ""))
	if name_zh != "":
		print("[MainGame] ★到达地标: %s — %s" % [name_zh, desc])
	else:
		print("[MainGame] 经过: %s" % desc)

	# 大地标触发绑定事件
	if event_id != "":
		var ev = EventSystem.get_event(event_id)
		if not ev.is_empty():
			event_dialog.show_event(ev)

## ===== 天色平滑渐变（核心）=====
## 根据当前精确小时(0-24)插值出叠加层颜色
func _update_day_night_smooth():
	var h = TimeSystem.get_hour_float()
	day_night_overlay.color = _get_overlay_color(h)

## 根据小时计算叠加色（连续渐变）
func _get_overlay_color(h: float) -> Color:
	var night = Color(0.03, 0.06, 0.14, 0.68)
	var predawn = Color(0.10, 0.10, 0.22, 0.55)
	var sunrise = Color(1.0, 0.55, 0.30, 0.30)
	var day = Color(1, 1, 1, 0.0)
	var sunset = Color(1.0, 0.45, 0.20, 0.32)
	var dusk = Color(0.35, 0.20, 0.35, 0.50)

	if h < 5.0:
		return night.lerp(predawn, h / 5.0)
	elif h < 6.5:
		return predawn.lerp(sunrise, (h - 5.0) / 1.5)
	elif h < 8.0:
		return sunrise.lerp(day, (h - 6.5) / 1.5)
	elif h < 16.5:
		return day
	elif h < 18.0:
		return day.lerp(sunset, (h - 16.5) / 1.5)
	elif h < 19.5:
		return sunset.lerp(dusk, (h - 18.0) / 1.5)
	elif h < 21.0:
		return dusk.lerp(night, (h - 19.5) / 1.5)
	else:
		return night

## ===== 被动衰减：每游戏小时触发 =====
func _on_hour_passed(_hour: int):
	GameManager.food = max(0, GameManager.food - 1.0)
	GameManager.water = max(0, GameManager.water - 1.3)
	GameManager.energy = max(0, GameManager.energy - 0.8)

	var target_temp = 30 if LocationSystem.current_segment == LocationSystem.Segment.ANDES else 60
	GameManager.temperature += (target_temp - GameManager.temperature) * 0.05

	if GameManager.food <= 0:
		GameManager.health = max(0, GameManager.health - 2)
	if GameManager.water <= 0:
		GameManager.health = max(0, GameManager.health - 2)

	status_panel.refresh_status()

	if GameManager.health <= 0:
		_on_game_over()

## ===== 行动 =====
func _on_action_btn_pressed():
	action_menu.show_menu()

func _on_action_selected(action_id: String):
	print("[MainGame] 结算行动: %s" % action_id)

	match action_id:
		"行军":
			_resolve_march()
		"狩猎":
			_resolve_hunt()
		"捕鱼":
			_resolve_fish()
		"采集":
			_resolve_forage()
		"rest":
			_resolve_rest()
		"camp":
			_resolve_camp()
		_:
			print("[MainGame] 行动 %s 暂未实现" % action_id)

	status_panel.refresh_status()

## 行军：消耗体力+快进时间+推进里程+换行进图
## 夜间行军：有头灯则正常，无头灯则距离打折+额外体力消耗(摸黑赶路)
func _resolve_march():
	GameManager.stamina = max(0, GameManager.stamina - 12)
	GameManager.food = max(0, GameManager.food - 5)
	GameManager.water = max(0, GameManager.water - 6)
	GameManager.energy = max(0, GameManager.energy - 5)

	var base_km = randf_range(5.0, 8.0)
	var terrain_factor = 0.6 if LocationSystem.current_segment == LocationSystem.Segment.ANDES else 1.0
	var actual_km = base_km * terrain_factor

	# 夜间行军：检查头灯
	var night_note = ""
	if TimeSystem.is_night():
		if GameManager.get_owned_count("headlamp") > 0:
			# 有头灯：夜间正常行军（无惩罚）
			night_note = " [夜·头灯照明]"
		else:
			# 无头灯摸黑：距离-50%，额外体力-8，健康小概率受伤
			actual_km *= 0.5
			GameManager.stamina = max(0, GameManager.stamina - 8)
			if randf() < 0.15:
				GameManager.health = max(0, GameManager.health - 5)
				night_note = " [夜·摸黑赶路，磕碰受伤-5]"
			else:
				night_note = " [夜·摸黑赶路，距离减半]"

	# 行军计数+1，换下一张行进图
	var seg = LocationSystem.get_segment_name()
	_march_index[seg] = _march_index.get(seg, 0) + 1
	_show_march_image()

	LocationSystem.advance_distance(actual_km)
	TimeSystem.skip_hours(4.0)  # 行军占4小时
	print("[MainGame] 行军 %.1fkm (第%d次)%s" % [actual_km, _march_index[seg], night_note])

func _resolve_hunt():
	GameManager.stamina = max(0, GameManager.stamina - 10)
	GameManager.energy = max(0, GameManager.energy - 5)
	if randf() < 0.3:
		print("[MainGame] 狩猎成功！获得meat×1")
	else:
		print("[MainGame] 狩猎失败")
	TimeSystem.skip_hours(3.0)

func _resolve_fish():
	GameManager.stamina = max(0, GameManager.stamina - 5)
	GameManager.energy = max(0, GameManager.energy - 3)
	if randf() < 0.25:
		var fish_type = "glowing_fish" if TimeSystem.is_night() else "fish"
		print("[MainGame] 捕鱼成功！获得%s×1" % fish_type)
	else:
		print("[MainGame] 捕鱼失败")
	TimeSystem.skip_hours(3.0)

func _resolve_forage():
	GameManager.stamina = max(0, GameManager.stamina - 6)
	if randf() < 0.7:
		var items = ["fruit", "mushroom", "wood"]
		var item = items[randi() % items.size()]
		print("[MainGame] 采集成功！获得%s×1" % item)
	else:
		print("[MainGame] 采集失败")
	TimeSystem.skip_hours(2.0)

func _resolve_rest():
	GameManager.stamina = min(100, GameManager.stamina + 15)
	GameManager.energy = min(100, GameManager.energy + 10)
	TimeSystem.skip_hours(2.0)
	print("[MainGame] 短歇，体力+15 精力+10")

func _resolve_camp():
	GameManager.stamina = min(100, GameManager.stamina + 40)
	GameManager.energy = min(100, GameManager.energy + 30)
	TimeSystem.skip_to_next_morning(6)
	print("[MainGame] 扎营过夜，体力+40 精力+30，跳到次日清晨")

## ===== 视觉更新 =====
func _update_weather_effects(_weather):
	match TimeSystem.weather:
		TimeSystem.Weather.RAIN:
			rain_particles.emitting = true
		_:
			rain_particles.emitting = false

func _on_segment_changed(_segment):
	# 进入新路段，重置该段行军计数，显示新路段第一张行进图
	_show_march_image()

func _on_inventory_btn_pressed():
	inventory_panel.show_inventory()

func _on_item_used(_item_id: String):
	status_panel.refresh_status()

func _on_game_over():
	TimeSystem.stop_clock()
	print("[MainGame] !!! 游戏结束：健康归零")
	# TODO: 显示游戏结束界面
