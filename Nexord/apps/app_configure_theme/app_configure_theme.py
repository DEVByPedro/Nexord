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
		page.bgcolor = "#E8EDF5"
		tempo_button = "#1a1a1a"
		button_color = "#FFFFFF"
		button_hover_color = "#EEF2F7"
		button_card_color = "#D9E2F0"
		text_color = "#172033"
		card_color = "#FFFFFF"
		container_color = "#F7F9FC"
		leftbar_color = "#F1F4F8"
		tempos_active_button = "#22C55E"
		tempos_active_button_hover = "#16A34A"
		color_border_textfield = "#000000"
		color_border_textfield_wrong = "#f52a48"
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
		container_color = "#1d2333"
		leftbar_color = "#0F141A"
		tempos_active_button = "#818CF8"
		tempos_active_button_hover = "#6366F1"
		color_border_textfield = "#ffffff"
		color_border_textfield_wrong = "#f52a48"
		set_user_current_theme("dark")

	# Atualiza todos os controles da página

	def update_control(control):

		if control is None:
			return

			# =========================
			# CONTROLE ATUAL
			# =========================

		if isinstance(control, ft.Button):
			control.bgcolor = button_color
			control.color = text_color

			if control.style:
				control.style.mouse_cursor = ft.MouseCursor.CLICK

			if control.data == "hovered_button":
				control.bgcolor = button_hover_color

			if control.data == "card_button":
				control.bgcolor = button_card_color

			if control.data == "close_button":
				control.bgcolor = "red"

		elif isinstance(control, ft.Text):
			control.color = text_color

		elif isinstance(control, ft.CircleAvatar):
			control.bgcolor = get_current_textcolor(theme)

		elif isinstance(control, ft.VerticalDivider):
			control.color = button_hover_color

		elif isinstance(control, ft.Container):
			control.bgcolor = card_color

			if control.data == "leftbar":
				control.bgcolor = leftbar_color

			elif control.data == "tempos_active_button":
				control.bgcolor = tempos_active_button

			elif control.data == "card_container":
				control.bgcolor = container_color

			elif control.data == "card_container_above":
				control.bgcolor = container_color
				control.border = ft.Border.all(1, "#444444")

			elif control.data == "tempo_button":
				control.bgcolor = tempo_button

		elif isinstance(control, ft.TextField):
			control.label_style = ft.TextStyle(color=color_border_textfield)
			control.border_color = color_border_textfield
			control.focused_border_color = color_border_textfield
			control.cursor_color = color_border_textfield

			if control.data == "field_wrong":
				control.label_style = ft.TextStyle(color=color_border_textfield_wrong)
				control.border_color = color_border_textfield_wrong
				control.focused_border_color = color_border_textfield_wrong
				control.cursor_color = color_border_textfield_wrong

		elif isinstance(control, ft.Icon):
			if control.data == "leftbar_button_icon":
				control.color = text_color

		controls = getattr(control, "controls", None)

		if isinstance(controls, (list, tuple)):
			for child in controls:
				update_control(child)

		# =========================
		# CONTENT
		# =========================

		content = getattr(control, "content", None)

		if content is not None:
			update_control(content)

		# =========================
		# ALERT DIALOG
		# =========================

		if isinstance(control, ft.AlertDialog):

			if control.title is not None:
				update_control(control.title)

			if control.content is not None:
				update_control(control.content)

			if control.actions:
				for action in control.actions:
					update_control(action)

	for control in page.controls:
		update_control(control)

	page.update()

def swap_theme(page):
	if page.theme_mode == ft.ThemeMode.LIGHT:
		set_theme(page, "dark")
	else:
		set_theme(page, "light")

	page.update()
