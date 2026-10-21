# TranslationSystem.gd
# 多语言翻译系统
extends Node

var current_language: String = "zh"  # 默认中文
var translations: Dictionary = {}

func _ready():
	load_language(current_language)
	print("TranslationSystem initialized, language: ", current_language)

# 加载语言文件
func load_language(lang: String):
	var file_path = "res://localization/" + lang + ".json"

	if not FileAccess.file_exists(file_path):
		print("Language file not found: ", file_path)
		# 使用内置的基础翻译
		translations = get_default_translations(lang)
		return

	var file = FileAccess.open(file_path, FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		var json = JSON.new()
		var error = json.parse(json_string)

		if error == OK:
			translations = json.data
			current_language = lang
			print("Language loaded: ", lang)
		else:
			print("JSON Parse Error: ", json.get_error_message())

		file.close()
	else:
		print("Failed to open language file: ", file_path)

# 翻译文本（使用 t 代替 tr 避免冲突）
func t(key: String) -> String:
	if translations.has(key):
		return translations[key]
	else:
		return key  # 找不到就返回key本身

# 切换语言
func switch_language(lang: String):
	load_language(lang)
	# 通知所有UI刷新文本
	get_tree().call_group("ui_text", "refresh_text")

# 获取默认翻译（内置）
func get_default_translations(lang: String) -> Dictionary:
	if lang == "zh":
		return {
			"ui.main_menu.title": "徒步亚马逊：赛博徒步",
			"ui.main_menu.new_game": "新游戏",
			"ui.main_menu.continue": "继续游戏",
			"ui.main_menu.achievements": "成就",
			"ui.main_menu.settings": "设置",
			"ui.main_menu.help": "帮助",
			"ui.main_menu.quit": "退出游戏",
			"ui.main_menu.language": "语言",
			"ui.difficulty.easy": "简单",
			"ui.difficulty.normal": "正常",
			"ui.difficulty.hard": "困难",
		}
	else:  # en
		return {
			"ui.main_menu.title": "Walking the Amazon: Cyber Trek",
			"ui.main_menu.new_game": "New Game",
			"ui.main_menu.continue": "Continue",
			"ui.main_menu.achievements": "Achievements",
			"ui.main_menu.settings": "Settings",
			"ui.main_menu.help": "Help",
			"ui.main_menu.quit": "Quit",
			"ui.main_menu.language": "Language",
			"ui.difficulty.easy": "Easy",
			"ui.difficulty.normal": "Normal",
			"ui.difficulty.hard": "Hard",
		}
