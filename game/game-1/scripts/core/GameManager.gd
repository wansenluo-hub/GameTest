# GameManager.gd
# 游戏全局管理器 - 单例
extends Node

# 游戏状态
enum GameState {
	MAIN_MENU,
	CHARACTER_CREATE,
	PLAYING,
	PAUSED,
	GAME_OVER
}

var current_state: GameState = GameState.MAIN_MENU

# 玩家信息
var player_name: String = ""
var start_date: Dictionary = {}  # {year, month, day}
var difficulty: String = "normal"  # easy, normal, hard

# 经济与背包
var money: int = 0
var inventory: Dictionary = {}      # item_id -> 数量
var current_weight: float = 0.0     # 当前负重(kg)
var max_weight: float = 50.0        # 最大负重(kg)

# 6状态 + 体温 (0-100)
var stamina: float = 80.0     # 体力
var energy: float = 90.0      # 精力
var food: float = 75.0        # 饱食度
var water: float = 80.0       # 水分
var health: float = 100.0     # 健康
var temperature: float = 60.0 # 体温(0寒冷 50正常 100过热)

# 当前路段（供TimeSystem等访问）
var current_segment: String = "andes"

# 游戏配置
var game_config = {
	"easy": {
		"initial_money": 3000,
		"state_decay_rate": 0.7,
		"event_danger_rate": 0.4,
		"item_price_rate": 0.8,
		"max_days": -1  # 无限制
	},
	"normal": {
		"initial_money": 2000,
		"state_decay_rate": 1.0,
		"event_danger_rate": 0.6,
		"item_price_rate": 1.0,
		"max_days": -1
	},
	"hard": {
		"initial_money": 1200,
		"state_decay_rate": 1.3,
		"event_danger_rate": 0.8,
		"item_price_rate": 1.2,
		"max_days": 1200
	}
}

func _ready():
	print("GameManager initialized")

# 开始新游戏
func start_new_game(p_name: String, p_start_date: Dictionary, p_difficulty: String):
	player_name = p_name
	start_date = p_start_date
	difficulty = p_difficulty

	# 按难度初始化经济与背包
	money = get_config("initial_money")
	inventory.clear()
	current_weight = 0.0

	# 初始化6状态+体温
	stamina = 80.0
	energy = 90.0
	food = 75.0
	water = 80.0
	health = 100.0
	temperature = 60.0

	current_state = GameState.PLAYING
	print("Game started: ", player_name, " on ", start_date, " difficulty: ", difficulty, " money: ", money)

	# TODO: 初始化其他系统
	# TimeSystem.initialize(start_date)
	# PlayerState.initialize(game_config[difficulty])

# ---- 存档 ----
# 是否存在存档(目前仅检查存档文件，完整存读档为后续模块)
func has_save() -> bool:
	return FileAccess.file_exists("user://savegame.save")

# ---- 经济与购买 ----
# 是否买得起
func can_afford(item_id: String) -> bool:
	var item = DataManager.get_item(item_id)
	if item.is_empty():
		return false
	return money >= int(item.get("price", 0))

# 购买物品(成功返回true)
func buy_item(item_id: String) -> bool:
	var item = DataManager.get_item(item_id)
	if item.is_empty():
		return false
	var price = int(item.get("price", 0))
	if money < price:
		return false
	money -= price
	inventory[item_id] = inventory.get(item_id, 0) + 1
	current_weight += int(item.get("weight", 0)) / 1000.0  # 克转kg
	return true

# 取某物品已购数量
func get_owned_count(item_id: String) -> int:
	return inventory.get(item_id, 0)

# 暂停游戏
func pause_game():
	current_state = GameState.PAUSED
	get_tree().paused = true

# 继续游戏
func resume_game():
	current_state = GameState.PLAYING
	get_tree().paused = false

# 游戏结束
func game_over(cause: String):
	current_state = GameState.GAME_OVER
	print("Game Over: ", cause)

# 返回主菜单
func return_to_main_menu():
	current_state = GameState.MAIN_MENU
	get_tree().change_scene_to_file("res://scenes/ui/MainMenu.tscn")

# 获取当前配置
func get_config(key: String):
	return game_config[difficulty].get(key)
