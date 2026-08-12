import threading
from time import sleep

import flet as ft

from config.left_bar_config.LeftBarConfig import (swap_left_bar, get_width_from_leftbar_last_state,
                                                  check_leftbar_last_state, get_current_leftbar_state)
from apps.app_change_theme.app_change_theme import swap_theme, get_current_theme, set_theme
from config.user_config.UserConfig import get_bpm_cap

global other_page

other_page = ft.Container(expand=True)

def open_metronome(page):

	global metronome_running

	global other_page

	def verify_tempo(e, bpm):
		try:
			field = e.control

			value = "".join(char for char in field.value if char.isdigit())

			if value == "":
				field.value = 1
				field.update()

			if int(value) <= get_bpm_cap():
				field.value = int(value)

			if int(value) > get_bpm_cap():
				field.value = get_bpm_cap()

			bpm = field.value
			tempo_bpm_text.value = f"{bpm} mbps"
			tempo_bpm_text.update()
			field.update()
		except Exception:
			pass

	def elevate_counting(textfield: ft.TextField, bpm):
		if textfield.value >= 1 and textfield.value <= get_bpm_cap():
			textfield.value += 1
			bpm = textfield.value
			tempo_bpm_text.value = f"{bpm} BPM"
			tempo_bpm_text.update()

		textfield.update()

	def remove_counting(textfield: ft.TextField, bpm):
		if textfield.value > 1:
			textfield.value -= 1
			bpm = textfield.value
			tempo_bpm_text.value = f"{bpm} BPM"
			tempo_bpm_text.update()

		textfield.update()

	def run_metronome(button, tempos_button, current_tempo, bpm_field):
		global metronome_running

		while metronome_running:

			bpm = int(bpm_field.value)
			interval = 60 / bpm

			current_tempo += 1

			if current_tempo > 4:
				current_tempo = 1

			tempos_button.controls[current_tempo - 1].key = "tempos_active_button"

			if current_tempo > 1:
				tempos_button.controls[current_tempo - 2].key = "tempos_button"
			else:
				tempos_button.controls[3].key = "tempos_button"

			set_theme(page, get_current_theme())
			page.update()

			print(f"BPM: {bpm} | Intervalo: {interval:.3f}s")

			sleep(interval)

	def start_tempo(button: ft.Button, tempos_button: ft.Row, current_tempo, bpm_field):
		global metronome_running

		if not metronome_running:
			metronome_running = True
			button.text = "Stop Metronome"

			for i in range(tempo):
				tempos_button.controls[i].key = "tempos_button"

			set_theme(page, get_current_theme())
			page.update()

			threading.Thread(
				target=run_metronome,
				args=(button, tempos_button, current_tempo, bpm_field),
				daemon=True
			).start()

		else:
			metronome_running = False
			button.text = "Start Metronome"
			page.update()

	metronome_running = False

	BPM = 1
	tempos_button = ft.Row(
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		tight=True,
		spacing=10
	)
	tempo_bpm_text = ft.Text(f"{BPM} BPM", size=50)
	choose_tempo_field = ft.TextField(width=100, value=1, on_change=lambda e: verify_tempo(e, BPM))
	less_button = ft.Button("-",
	                        on_click=lambda e: remove_counting(choose_tempo_field, BPM),
	                        height=choose_tempo_field.height,
							style = ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	                        )
	more_button = ft.Button("+",
	                        on_click=lambda e: elevate_counting(choose_tempo_field, BPM),
	                        height=choose_tempo_field.height,
	                        style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	                        )
	start_tempo_button = ft.Button(
		"Start Metronome",
		style=ft.ButtonStyle(
			shape={"": ft.RoundedRectangleBorder(radius=5)},
			padding=15
		),
		on_click=lambda e: start_tempo(
			start_tempo_button,
			tempos_button,
			current_tempo,
			choose_tempo_field
		)
	)

	tempo = 4
	current_tempo = 0
	for i in range(tempo):
		tempos_button.controls.append(
			ft.Container(
				key="tempos_button",
				bgcolor="green",
				width=10,
				height=10,
				border_radius=50
			)
		)

	other_page.content = ft.Column(
		[
			ft.Container(),
			ft.Text(
				"Metronome",
				size=30,
			),

			ft.Container(
				content=ft.Column(
					[
						tempo_bpm_text,

						tempos_button,

						ft.Row(
							[
								less_button,
								choose_tempo_field,
								more_button,
							],
							alignment=ft.MainAxisAlignment.CENTER,
						),
					],
					spacing=20,
					horizontal_alignment=ft.CrossAxisAlignment.CENTER,
					alignment=ft.MainAxisAlignment.CENTER
				),
			),

			start_tempo_button,
			ft.Container()
		],
		key="leftbar_buttons",
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		expand=True,
	)

	set_theme(page, get_current_theme())
	page.update()

def open_tuner():
	pass

def open_escale():
	pass

def get_icon_theme():
	current_theme = get_current_theme()
	if current_theme == "light":
		return ft.Icons.DARK_MODE
	return ft.Icons.LIGHT_MODE

def swap_theme_button(page, icon):
	swap_theme(page)
	icon.name = get_icon_theme()
	icon.update()

def configure_left_bar_button(page: ft.Page):
	top_buttons = ft.Column(
		spacing=10,
		horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
	)

	top_buttons_icons_text = [("Home", ft.Icons.MENU)]

	for i, (text, icon) in enumerate(top_buttons_icons_text):
		top_buttons.controls.append(
			ft.Button(
				content=ft.Row(
					[
						ft.Icon(icon, key="leftbar_button_icon"),
						ft.Text(text, key="leftbar_text"),
					],
					spacing=10,
					alignment=ft.MainAxisAlignment.START,
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					expand=True,
				),
				on_click=lambda e: swap_left_bar(page),
				style=ft.ButtonStyle(
					shape={"": ft.RoundedRectangleBorder(radius=5)}
				),
			)
		)

	middle_buttons = ft.Column(
		spacing=10,
		horizontal_alignment=ft.CrossAxisAlignment.STRETCH
	)

	middle_buttons_text_icons = [
		("Afinador", ft.Icons.MIC),
		("Escalas", ft.Icons.MUSIC_NOTE),
		("Metronomo", ft.Icons.TIMER)]

	for i, (text, icon) in enumerate(middle_buttons_text_icons):
		middle_buttons.controls.append(
			ft.Button(
				content=ft.Row(
					[
						ft.Icon(icon, key="leftbar_button_icon"),
						ft.Text(text, key="leftbar_text"),
					],
					spacing=10,
					alignment=ft.MainAxisAlignment.START,
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					expand=True,
				),
				on_click=lambda e, index=i: print(f"Button {index + 1}"),
				style=ft.ButtonStyle(
					shape={
						"": ft.RoundedRectangleBorder(radius=5)
					}
				),
			)
		)

		if text == "Metronomo":
			middle_buttons.controls[i].on_click = lambda e: open_metronome(page)

	bottom_buttons = ft.Column(
		spacing=10,
		horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
	)

	bottom_buttons_text_icon = [
		("Mudar Tema", get_icon_theme()),
		("Perfil", ft.Icons.PERSON),
	]

	for i, (text, icon) in enumerate(bottom_buttons_text_icon):
		bottom_buttons.controls.append(
			ft.Button(
				content=ft.Row(
					[
						ft.Icon(icon, key="leftbar_button_icon"),
						ft.Text(text, key="leftbar_text"),
					],
					spacing=10,
					alignment=ft.MainAxisAlignment.START,
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					expand=True,
				),
				style=ft.ButtonStyle(
					shape={"": ft.RoundedRectangleBorder(radius=5)},
				),
			)
		)

		if text == "Mudar Tema":
			bottom_buttons.controls[i].on_click = lambda e, index=i: swap_theme_button(
				page,
				bottom_buttons.controls[index].content.controls[0]
			)

	buttons = ft.Column(
		key="leftbar_buttons",
		controls=[
			top_buttons,
			middle_buttons,
			bottom_buttons,
		],
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		expand=True
	)

	return buttons

def configure_left_bar(page: ft.Page):
	leftbar_buttons = configure_left_bar_button(page)

	left_bar = ft.Container(
		key="leftbar",
		content=leftbar_buttons,
		width=get_width_from_leftbar_last_state(page),
		padding=20,
	)

	return left_bar

def configure_main_window(page: ft.Page):
	global other_page

	left_bar = configure_left_bar(page)

	main_window = ft.Row([
		left_bar,
		other_page,
	], expand=True, spacing=0)

	return main_window, left_bar

def configure_application_css(page: ft.Page):
	main_window, left_bar = configure_main_window(page)

	page.add(main_window)

	def on_resize(e: ft.WindowResizeEvent):
		if get_current_leftbar_state():
			left_bar.width = e.width * 0.20
		elif not get_current_leftbar_state() and page.window.maximized:
			left_bar.width = e.width * 0.04

		page.update()

	check_leftbar_last_state(page)
	page.on_resized = on_resize
