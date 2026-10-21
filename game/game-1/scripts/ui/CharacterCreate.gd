# CharacterCreate.gd
# 角色创建界面：输入名字 + 选择难度 -> 开始游戏进入商店
extends Control

var selected_difficulty: String = "normal"

# ---- 配色(参考案例图:近纯黑底+青翡翠霓虹+白字) ----
const C_BG := Color("05080a")
const C_PANEL := Color("0c1316")
const C_PANEL_HI := Color("122024")
const C_NEON := Color("00e5c0")
const C_CYAN := Color("1ad6b4")
const C_TEXT := Color("e6f0ee")
const C_DIM := Color("5e7872")
const C_GOLD := Color("ffd24a")

@onready var title: Label = $Panel/VBox/Title
@onready var name_label: Label = $Panel/VBox/NameLabel
@onready var name_input: LineEdit = $Panel/VBox/NameInput
@onready var name_hint: Label = $Panel/VBox/NameHint
@onready var diff_label: Label = $Panel/VBox/DiffLabel
@onready var easy_btn: Button = $Panel/VBox/DiffBox/EasyBtn
@onready var normal_btn: Button = $Panel/VBox/DiffBox/NormalBtn
@onready var hard_btn: Button = $Panel/VBox/DiffBox/HardBtn
@onready var start_btn: Button = $Panel/VBox/StartBtn
@onready var back_btn: Button = $BackBtn

func _ready():
	_apply_theme()
	easy_btn.pressed.connect(func(): _select_difficulty("easy"))
	normal_btn.pressed.connect(func(): _select_difficulty("normal"))
	hard_btn.pressed.connect(func(): _select_difficulty("hard"))
	start_btn.pressed.connect(_on_start)
	back_btn.pressed.connect(_on_back)
	name_input.text_changed.connect(func(_t): _validate())

	_select_difficulty("normal")
	refresh_ui()
	_validate()

# ---- 样式 ----
func _neon_box(bg: Color, border: Color, width: int = 2, radius: int = 6) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(width)
	sb.set_corner_radius_all(radius)
	sb.set_content_margin_all(10)
	return sb

func _apply_theme():
	$ColorRect.color = C_BG
	$Panel.add_theme_stylebox_override("panel", _neon_box(C_PANEL, C_NEON, 2, 12))
	title.add_theme_color_override("font_color", C_NEON)
	name_label.add_theme_color_override("font_color", C_TEXT)
	diff_label.add_theme_color_override("font_color", C_TEXT)
	name_hint.add_theme_color_override("font_color", C_DIM)
	# 名字输入框
	name_input.add_theme_color_override("font_color", C_TEXT)
	name_input.add_theme_color_override("caret_color", C_NEON)
	name_input.add_theme_stylebox_override("normal", _neon_box(C_BG, C_DIM.darkened(0.2), 1, 6))
	name_input.add_theme_stylebox_override("focus", _neon_box(C_BG, C_NEON, 2, 6))
	# 难度按钮 + 开始 + 返回
	for b in [easy_btn, normal_btn, hard_btn]:
		_style_toggle(b)
	_style_action(start_btn)
	_style_action(back_btn)

func _style_toggle(btn: Button):
	btn.add_theme_color_override("font_color", C_DIM)
	btn.add_theme_color_override("font_pressed_color", C_BG)
	btn.add_theme_color_override("font_hover_color", C_NEON)
	btn.add_theme_stylebox_override("normal", _neon_box(C_PANEL, C_DIM.darkened(0.2), 1, 6))
	btn.add_theme_stylebox_override("hover", _neon_box(C_PANEL_HI, C_NEON, 1, 6))
	btn.add_theme_stylebox_override("pressed", _neon_box(C_NEON, C_NEON, 1, 6))

func _style_action(btn: Button):
	btn.add_theme_color_override("font_color", C_BG)
	btn.add_theme_color_override("font_hover_color", C_BG)
	btn.add_theme_stylebox_override("normal", _neon_box(C_NEON, C_NEON, 2, 8))
	btn.add_theme_stylebox_override("hover", _neon_box(C_CYAN, C_CYAN, 2, 8))
	btn.add_theme_stylebox_override("pressed", _neon_box(C_CYAN, C_NEON, 2, 8))

func refresh_ui():
	title.text = Translator.t("ui.character_create.title")
	name_label.text = Translator.t("ui.character_create.name")
	name_input.placeholder_text = Translator.t("ui.character_create.name")
	name_hint.text = Translator.t("ui.character_create.name_hint")
	diff_label.text = Translator.t("ui.character_create.select_difficulty")
	easy_btn.text = Translator.t("ui.difficulty.easy")
	normal_btn.text = Translator.t("ui.difficulty.normal")
	hard_btn.text = Translator.t("ui.difficulty.hard")
	start_btn.text = "🥾 " + Translator.t("ui.character_create.start")
	back_btn.text = "← " + Translator.t("ui.main_menu.title")
	_update_diff_hint()

func _select_difficulty(diff: String):
	selected_difficulty = diff
	easy_btn.button_pressed = (diff == "easy")
	normal_btn.button_pressed = (diff == "normal")
	hard_btn.button_pressed = (diff == "hard")
	_update_diff_hint()

func _update_diff_hint():
	var money = GameManager.game_config[selected_difficulty]["initial_money"]
	diff_label.text = Translator.t("ui.character_create.select_difficulty") + "   ◇ $" + str(money)

# 名字校验：2-12 字符
func _validate() -> bool:
	var n = name_input.text.strip_edges()
	var ok = n.length() >= 2 and n.length() <= 12
	start_btn.disabled = not ok
	return ok

func _on_start():
	if not _validate():
		name_hint.text = Translator.t("ui.character_create.name_invalid")
		return
	var p_name = name_input.text.strip_edges()
	# 出发日期暂用默认(2030-06-15)，日期选择为后续模块
	var start_date = {"year": 2030, "month": 6, "day": 15}
	GameManager.start_new_game(p_name, start_date, selected_difficulty)
	get_tree().change_scene_to_file("res://scenes/ui/Shop.tscn")

func _on_back():
	get_tree().change_scene_to_file("res://scenes/ui/MainMenu.tscn")
