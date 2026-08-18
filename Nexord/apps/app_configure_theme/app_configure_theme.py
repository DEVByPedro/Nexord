import flet as ft
from config.user.user_preferences.UserConfig import set_user_current_theme

def get_current_theme():
	import json

	with open("config/user/json/user_json.json") as user_file:
		user_data = json.load(user_file)

	return user_data["current_theme"]

def get_current_textcolor(theme):

	text_color = ""
	if theme == "light":
		text_color = "#1a1a1a"
	elif theme == "dark":
		text_color = "#e6e6e6"

	return text_color

def set_theme(page, theme):
	if theme == "light":
		page.theme_mode = ft.ThemeMode.LIGHT
		page.bgcolor = "#fafafa"
		button_color = "#ffffff"
		button_hover_color = "#f0f0f0"
		text_color = "#1a1a1a"
		card_color = "#ffffff"
		leftbar_color = "#f5f5f5"
		tempos_active_button = "#16a34a"
		tempos_active_button_hover = "#15803d"
		set_user_current_theme("light")
	elif theme == "dark":
		page.theme_mode = ft.ThemeMode.DARK
		page.bgcolor = "#0d1117"
		button_color = "#161b22"
		button_hover_color = "#21262d"
		text_color = "#e6e6e6"
		card_color = "#161b22"
		leftbar_color = "#0d1117"
		tempos_active_button = "#818cf8"
		tempos_active_button_hover = "#6366f1"
		set_user_current_theme("dark")

	# Atualiza todos os controles da página

	def update_control(control):
		if isinstance(control, ft.Button):
			control.bgcolor = button_color
			control.color = text_color

			if control.key == "hovered_button":
				control.bgcolor = button_hover_color

		elif isinstance(control, ft.Text):
			control.color = text_color

		elif isinstance(control, ft.Container):
			control.bgcolor = card_color
			if control.key == "leftbar":
				control.bgcolor = leftbar_color
			if control.key == "tempos_active_button":
				control.bgcolor = tempos_active_button

		elif isinstance(control, ft.Icon):
			if control.key == "leftbar_button_icon":
				control.color = text_color

		# Controles filhos
		if hasattr(control, "controls"):
			for child in control.controls:
				update_control(child)

		if hasattr(control, "content") and control.content:
			update_control(control.content)

	for control in page.controls:
		update_control(control)

	page.update()

def swap_theme(page):
	if page.theme_mode == ft.ThemeMode.LIGHT:
		set_theme(page, "dark")
	else:
		set_theme(page, "light")

	page.update()
