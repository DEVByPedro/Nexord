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
		page.bgcolor = "#F7F9FC"
		tempo_button = "#1a1a1a"
		button_color = "#FFFFFF"
		button_hover_color = "#EEF2F7"
		button_card_color = "#D9E2F0"
		text_color = "#172033"
		card_color = "#FFFFFF"
		container_color = "#E8EDF5"
		leftbar_color = "#F1F4F8"
		tempos_active_button = "#22C55E"
		tempos_active_button_hover = "#16A34A"
		set_user_current_theme("light")
	elif theme == "dark":
		page.theme_mode = ft.ThemeMode.DARK
		page.bgcolor = "#0B0F14"
		tempo_button = "#e6e6e6"
		button_color = "#151B23"
		button_hover_color = "#202832"
		button_card_color = "#303B4D"
		text_color = "#E6EDF3"
		card_color = "#151B23"
		container_color = "#1C2530"
		leftbar_color = "#0F141A"
		tempos_active_button = "#818CF8"
		tempos_active_button_hover = "#6366F1"
		set_user_current_theme("dark")

	# Atualiza todos os controles da página

	def update_control(control):
		if isinstance(control, ft.Button):
			control.bgcolor = button_color
			control.color = text_color
			control.style.mouse_cursor = ft.MouseCursor.CLICK

			if control.key == "hovered_button":
				control.bgcolor = button_hover_color

			if control.key == "card_button":
				control.bgcolor = button_card_color

		elif isinstance(control, ft.Text):
			control.color = text_color

		elif isinstance(control, ft.VerticalDivider):
			control.color = button_hover_color

		elif isinstance(control, ft.Container):
			control.bgcolor = card_color
			if control.key == "leftbar":
				control.bgcolor = leftbar_color
			if control.key == "tempos_active_button":
				control.bgcolor = tempos_active_button
			if control.key == "card_container":
				control.bgcolor=container_color
			if control.key == "tempo_button":
				control.bgcolor = tempo_button

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
