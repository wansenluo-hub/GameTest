# MainMenu.gd
# 主菜单界面脚本
extends Control

func _ready():
	# 连接按钮信号
	$VBox/NewGameBtn.pressed.connect(_on_new_game)
	$VBox/ContinueBtn.pressed.connect(_on_continue)
	$VBox/AchievementsBtn.pressed.connect(_on_achievements)
	$VBox/SettingsBtn.pressed.connect(_on_settings)
	$VBox/HelpBtn.pressed.connect(_on_help)
	$VBox/QuitBtn.pressed.connect(_on_quit)
	$LanguageBtn.pressed.connect(_on_language)

	refresh_ui()

	# 无存档时禁用"继续游戏"
	$VBox/ContinueBtn.disabled = not GameManager.has_save()

func refresh_ui():
	$Title.text = Translator.t("ui.main_menu.title")
	$VBox/NewGameBtn.text = "🎮 " + Translator.t("ui.main_menu.new_game")
	$VBox/ContinueBtn.text = "📁 " + Translator.t("ui.main_menu.continue")
	$VBox/AchievementsBtn.text = "🏆 " + Translator.t("ui.main_menu.achievements")
	$VBox/SettingsBtn.text = "⚙️ " + Translator.t("ui.main_menu.settings")
	$VBox/HelpBtn.text = "❓ " + Translator.t("ui.main_menu.help")
	$VBox/QuitBtn.text = "🚪 " + Translator.t("ui.main_menu.quit")
	$LanguageBtn.text = "🌐 " + ("EN" if Translator.current_language == "zh" else "中文")

func _on_new_game():
	get_tree().change_scene_to_file("res://scenes/ui/CharacterCreate.tscn")

func _on_continue():
	if GameManager.has_save():
		print("Continue - load save (TODO)")
	else:
		print("No save available")

func _on_achievements():
	print("Achievements")

func _on_settings():
	print("Settings")

func _on_help():
	print("Help")

func _on_quit():
	get_tree().quit()

func _on_language():
	Translator.switch_language("en" if Translator.current_language == "zh" else "zh")
	refresh_ui()
