extends Node
## TimeSystem - 实时流逝的时间系统 autoload
## 时间持续走动（挂机也走），显示时分秒，天色随时间平滑变化

# ===== 时间流速 =====
# 现实1秒 = 游戏 TIME_SCALE 秒。120 = 现实1秒走游戏2分钟，一天≈12分钟现实时间。
# 想更快/更慢改这里。
@export var TIME_SCALE: float = 120.0

# 时段枚举 (0-5)，从小时推导
enum TimeOfDay { DAWN, MORNING, NOON, AFTERNOON, DUSK, NIGHT }
const TIME_NAMES_ZH = ["凌晨", "清晨", "上午", "午后", "黄昏", "夜晚"]

enum Season { DRY, WET }
enum Weather { CLEAR, CLOUDY, RAIN, FOG, SNOW }

# ===== 核心：游戏总秒数 =====
# 开局第1天 06:00:00（清晨6点出发）
var game_seconds: float = 6.0 * 3600.0

var season: Season = Season.DRY
var weather: Weather = Weather.CLEAR
const RAINY_SEASON_START_DAY = 90

# 时钟是否在走（进入主游戏才开始）
var running: bool = false

# 上一帧的整点小时/时段/天，用于检测跨越
var _last_hour: int = -1
var _last_tod: int = -1
var _last_day: int = -1

# 信号
signal hour_passed(new_hour: int)          # 每过1游戏小时（用于被动衰减）
signal time_of_day_changed(new_tod: int)   # 时段切换
signal day_passed(new_day: int)            # 跨天
signal season_changed(new_season: Season)
signal weather_changed(new_weather: Weather)

func _ready():
	_last_hour = get_hour()
	_last_tod = get_time_of_day()
	_last_day = get_day()
	print("[TimeSystem] ready: %s 时钟暂停中" % get_clock_string())

func _process(delta):
	if not running:
		return

	game_seconds += delta * TIME_SCALE

	# 检测跨小时
	var h = get_hour()
	if h != _last_hour:
		_last_hour = h
		hour_passed.emit(h)
		_roll_weather()  # 每小时roll一次天气

	# 检测时段切换
	var tod = get_time_of_day()
	if tod != _last_tod:
		_last_tod = tod
		time_of_day_changed.emit(tod)

	# 检测跨天
	var d = get_day()
	if d != _last_day:
		_last_day = d
		day_passed.emit(d)
		_on_new_day(d)

## 启动/暂停时钟
func start_clock():
	running = true
	print("[TimeSystem] 时钟启动 @ %s" % get_clock_string())

func stop_clock():
	running = false

## 快进时间（行动消耗）
func skip_hours(hours: float):
	# 逐小时推进，确保每个跨越的信号都触发
	var target = game_seconds + hours * 3600.0
	while game_seconds < target:
		var step = min(3600.0, target - game_seconds)
		game_seconds += step
		var h = get_hour()
		if h != _last_hour:
			_last_hour = h
			hour_passed.emit(h)
			_roll_weather()
		var tod = get_time_of_day()
		if tod != _last_tod:
			_last_tod = tod
			time_of_day_changed.emit(tod)
		var d = get_day()
		if d != _last_day:
			_last_day = d
			day_passed.emit(d)
			_on_new_day(d)
	print("[TimeSystem] 快进%.1f小时 -> %s" % [hours, get_clock_string()])

## 快进到次日指定小时（扎营用）
func skip_to_next_morning(morning_hour: int = 6):
	var cur_h = get_seconds_in_day() / 3600.0
	var hours_to_skip: float
	if cur_h < morning_hour:
		hours_to_skip = morning_hour - cur_h
	else:
		hours_to_skip = (24 - cur_h) + morning_hour
	skip_hours(hours_to_skip)

# ===== 时间推导 =====
func get_day() -> int:
	return int(game_seconds / 86400.0) + 1

func get_seconds_in_day() -> float:
	return fmod(game_seconds, 86400.0)

func get_hour() -> int:
	return int(get_seconds_in_day() / 3600.0)

func get_minute() -> int:
	return int(fmod(get_seconds_in_day(), 3600.0) / 60.0)

func get_second() -> int:
	return int(fmod(game_seconds, 60.0))

## 一天内的精确小时（0.0-24.0），用于天色平滑插值
func get_hour_float() -> float:
	return get_seconds_in_day() / 3600.0

## 时段从小时推导
func get_time_of_day() -> int:
	var h = get_hour()
	if h < 4: return TimeOfDay.DAWN
	elif h < 8: return TimeOfDay.MORNING
	elif h < 12: return TimeOfDay.NOON
	elif h < 16: return TimeOfDay.AFTERNOON
	elif h < 20: return TimeOfDay.DUSK
	else: return TimeOfDay.NIGHT

# 兼容旧代码：time_of_day 作为属性访问
var time_of_day: int:
	get: return get_time_of_day()

var day: int:
	get: return get_day()

# ===== 显示字符串 =====
## HH:mm
func get_clock_string() -> String:
	return "%02d:%02d" % [get_hour(), get_minute()]

func get_time_name() -> String:
	return TIME_NAMES_ZH[get_time_of_day()]

func get_season_name() -> String:
	return "旱季" if season == Season.DRY else "雨季"

func get_weather_name() -> String:
	match weather:
		Weather.CLEAR: return "晴"
		Weather.CLOUDY: return "阴"
		Weather.RAIN: return "雨"
		Weather.FOG: return "雾"
		Weather.SNOW: return "雪"
	return "未知"

func is_daytime() -> bool:
	var h = get_hour()
	return h >= 7 and h < 18

func is_night() -> bool:
	var h = get_hour()
	return h < 6 or h >= 19

# ===== 内部 =====
func _on_new_day(d: int):
	if d == RAINY_SEASON_START_DAY and season == Season.DRY:
		season = Season.WET
		season_changed.emit(season)
		print("[TimeSystem] !!! 雨季开始 day=%d" % d)

func _roll_weather():
	var segment = LocationSystem.get_segment_name()
	var old_weather = weather

	if segment == "andes":
		weather = Weather.CLEAR if randf() < 0.7 else Weather.SNOW
	else:
		if season == Season.DRY:
			var r = randf()
			if r < 0.7: weather = Weather.CLEAR
			elif r < 0.9: weather = Weather.CLOUDY
			else: weather = Weather.RAIN
		else:
			var r = randf()
			if r < 0.6: weather = Weather.RAIN
			elif r < 0.9: weather = Weather.CLOUDY
			else: weather = Weather.CLEAR

	if weather != old_weather:
		weather_changed.emit(weather)
