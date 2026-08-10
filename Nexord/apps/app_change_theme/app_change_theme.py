import flet as ft
from config.user_config.UserConfig import set_user_current_theme

def get_current_theme():
	import json

	with open("config/user_config/user_json.json") as user_file:
		user_data = json.load(user_file)

	return user_data["current_theme"]


def set_theme(page, theme):
	if theme == "light":
		page.theme_mode = ft.ThemeMode.LIGHT
		page.bgcolor = "#f5f0f0"
		button_color = "#d1d1d1"
		text_color = "#000000"
		card_color = "#FFFFFF"
		leftbar_color = "#f0f0f0"
		set_user_current_theme("light")
	elif theme == "dark":
		page.theme_mode = ft.ThemeMode.DARK
		page.bgcolor = "#101420"
		button_color = "#1f242e"
		text_color = "#FFFFFF"
		card_color = "#11151f"
		leftbar_color = "#181d29"
		set_user_current_theme("dark")

	# Atualiza todos os controles da página

	def update_control(control):
		if isinstance(control, ft.Button):
			control.bgcolor = button_color
			control.color = text_color

		elif isinstance(control, ft.Text):
			control.color = text_color

		elif isinstance(control, ft.Container):
			control.bgcolor = card_color
			if control.key == "leftbar":
				control.bgcolor = leftbar_color

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
