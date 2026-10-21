extends PanelContainer
## StatusPanel - 状态显示面板
## 显示：时间/位置/6状态条/金钱/负重

@onready var day_label = $VBox/TopRow/DayLabel
@onready var time_label = $VBox/TopRow/TimeLabel
@onready var weather_label = $VBox/TopRow/WeatherLabel
@onready var location_label = $VBox/LocationRow/LocationLabel
@onready var distance_label = $VBox/LocationRow/DistanceLabel

# 6状态条
@onready var stamina_bar = $VBox/StatsGrid/StaminaBar
@onready var energy_bar = $VBox/StatsGrid/EnergyBar
@onready var food_bar = $VBox/StatsGrid/FoodBar
@onready var water_bar = $VBox/StatsGrid/WaterBar
@onready var health_bar = $VBox/StatsGrid/HealthBar
@onready var temperature_bar = $VBox/StatsGrid/TemperatureBar

@onready var money_label = $VBox/BottomRow/MoneyLabel
@onready var weight_label = $VBox/BottomRow/WeightLabel

func _ready():
	# 连接信号
	TimeSystem.time_of_day_changed.connect(_on_tod_changed)
	TimeSystem.weather_changed.connect(_on_weather_changed)
	TimeSystem.day_passed.connect(_on_day_passed)
	LocationSystem.distance_changed.connect(_on_distance_changed)
	LocationSystem.segment_changed.connect(_on_segment_changed)

	# 初始显示
	_refresh_all()

## 每帧刷新时钟（实时流逝的时分秒）
func _process(_delta):
	day_label.text = "第%d天" % TimeSystem.get_day()
	time_label.text = "%s %s" % [TimeSystem.get_clock_string(), TimeSystem.get_time_name()]

func _refresh_all():
	_update_time_display()
	_update_location_display()
	_update_status_bars()
	_update_money_weight()

func _on_tod_changed(_tod):
	_update_time_display()

func _on_day_passed(_day):
	_update_time_display()

func _on_weather_changed(_weather):
	_update_time_display()

func _on_distance_changed(_km):
	_update_location_display()

func _on_segment_changed(_seg):
	_update_location_display()

func _update_time_display():
	day_label.text = "第%d天" % TimeSystem.get_day()
	time_label.text = "%s %s" % [TimeSystem.get_clock_string(), TimeSystem.get_time_name()]
	weather_label.text = "%s · %s" % [TimeSystem.get_season_name(), TimeSystem.get_weather_name()]

func _update_location_display():
	location_label.text = LocationSystem.get_segment_name_zh()
	distance_label.text = "%.1f km / 9600 km" % LocationSystem.total_distance

func _update_status_bars():
	stamina_bar.value = GameManager.stamina
	energy_bar.value = GameManager.energy
	food_bar.value = GameManager.food
	water_bar.value = GameManager.water
	health_bar.value = GameManager.health
	temperature_bar.value = GameManager.temperature

func _update_money_weight():
	money_label.text = "$%d" % GameManager.money
	weight_label.text = "%.1f / %.1f kg" % [GameManager.current_weight, GameManager.max_weight]

## 外部调用：刷新状态条
func refresh_status():
	_update_status_bars()
	_update_money_weight()
