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
			tempo_bpm_text.value = f"{bpm} BPM"
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

	def increase_compass_tempo_counting(e, textfield):
		value = int(textfield.value or 0)

		if value > 0 and value < 12:
			value += 1

		textfield.value = str(value)
		update_compass_tempo_buttons()
		textfield.update()

	def decrease_compass_tempo_counting(e, textfield):
		value = int(textfield.value or 0)

		if value > 1:
			value -= 1

		textfield.value = str(value)
		update_compass_tempo_buttons()
		textfield.update()

	def play_click():
		import sounddevice as sd
		import numpy as np

		sample_rate = 44100
		duration = 0.05
		frequency = 1000

		t = np.linspace(
			0,
			duration,
			int(sample_rate * duration),
			False
		)

		sound = 0.3 * np.sin(2 * np.pi * frequency * t)

		sd.play(sound, sample_rate, blocking=False)

	def play_strong_click():
		import sounddevice as sd
		import numpy as np

		sample_rate = 44100
		duration = 0.07
		frequency = 1500
		volume = 0.8

		t = np.linspace(
			0,
			duration,
			int(sample_rate * duration),
			endpoint=False
		)

		sound = np.sin(2 * np.pi * frequency * t)

		envelope = np.exp(-t * 60)

		sound = sound * envelope * volume

		sd.play(
			sound.astype(np.float32),
			sample_rate,
			blocking=False
		)

	def only_numbers(e):
		try:
			value = "".join(c for c in e.control.value if c.isdigit())

			if value == "":
				value = 1

			if int(e.control.value) > 12:
				value = 12

			if e.control.value != value:
				e.control.value = value
				e.control.update()

			update_compass_tempo_buttons()
		except ValueError:
			pass

	def update_compass_tempo_buttons():
		global metronome_running

		tempo = int(textfield_compass_tempo.value or 1)

		tempos_button.controls.clear()

		for i in range(tempo):
			tempos_button.controls.append(
				ft.Container(
					key="tempos_button",
					width=10,
					height=10,
					border_radius=50,
				)
			)

		set_theme(page, get_current_theme())

		# reset metronome
		metronome_running = False
		start_tempo_button.text = "Começar Metrónomo"
		page.update()

		tempos_button.update()

	def run_metronome(button, tempos_button, current_tempo, bpm_field, tempo):
		global metronome_running

		while metronome_running:

			bpm = int(bpm_field.value)
			interval = 60 / bpm

			current_tempo += 1

			if current_tempo > tempo:
				current_tempo = 1

			current_index = current_tempo - 1
			previous_index = (current_index - 1) % tempo

			tempos_button.controls[previous_index].key = "tempos_button"
			tempos_button.controls[current_index].key = "tempos_active_button"

			if current_tempo == 1:
				# play metronome strong sound
				play_strong_click()

			if current_tempo > 1:
				# play metronome sound
				play_click()

			set_theme(page, get_current_theme())
			page.update()

			sleep(interval)

	def start_tempo(button: ft.Button, tempos_button: ft.Row, current_tempo, bpm_field, tempo):
		global metronome_running

		if not metronome_running:
			metronome_running = True
			button.text = "Parar Metrónomo"

			for i in range(tempo):
				tempos_button.controls[i].key = "tempos_button"

			page.update()

			threading.Thread(
				target=run_metronome,
				args=(button, tempos_button, current_tempo, bpm_field, tempo),
				daemon=True
			).start()

		else:
			metronome_running = False
			button.text = "Começar Metrónomo"
			page.update()

	metronome_running = False

	BPM = 1
	tempos_button = ft.Row(
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		tight=True,
		spacing=10
	)

	textfield_compass_tempo = ft.TextField(hint_text="Max 12",
	                                       width=100,
	                                       value=4,
	                                       on_change=lambda e: only_numbers(e)
	)
	more_compass_tempo_choose = ft.Button("+",
	                                      style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
	                                      on_click= lambda e: increase_compass_tempo_counting(e, textfield_compass_tempo)
	                                      )
	less_compass_tempo_choose = ft.Button("-",
	                                      style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
	                                      on_click= lambda e: decrease_compass_tempo_counting(e, textfield_compass_tempo)
	                                      )

	tempo_list = ft.Column(
		[
			ft.Text(
				"Tempos por Compasso:",
				size=15,
				weight=ft.FontWeight.W_500,
				text_align=ft.TextAlign.CENTER,
			),

			ft.Row(
				[
					less_compass_tempo_choose,
					textfield_compass_tempo,
					more_compass_tempo_choose,
				],
				alignment=ft.MainAxisAlignment.CENTER,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=8,
			),
		],
		alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		spacing=10,
		tight=True,
	)

	tempo_bpm_text = ft.Text(f"{BPM} BPM", size=50)
	choose_tempo_field = ft.TextField(width=100, value=1, on_change=lambda e: verify_tempo(e, BPM))
	less_button = ft.Button("-",
	                        on_click=lambda e: remove_counting(choose_tempo_field, BPM),
	                        height=choose_tempo_field.height,
	                        style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	                        )
	more_button = ft.Button("+",
	                        on_click=lambda e: elevate_counting(choose_tempo_field, BPM),
	                        height=choose_tempo_field.height,
	                        style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	                        )

	tempo_rows = ft.Column(
		[
			ft.Text("Batidas por Minuto:",
			        size=15,
			        weight=ft.FontWeight.W_500,
			        text_align=ft.TextAlign.CENTER),
			ft.Row(
				[
					less_button,
					choose_tempo_field,
					more_button,
				],
				alignment=ft.MainAxisAlignment.CENTER,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=8,
			)
		],
		alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		spacing=10,
		tight=True,
	)
	start_tempo_button = ft.Button(
		"Começar Metrónomo",
		style=ft.ButtonStyle(
			shape={"": ft.RoundedRectangleBorder(radius=5)},
			padding=15
		),
		on_click=lambda e: start_tempo(
			start_tempo_button,
			tempos_button,
			current_tempo,
			choose_tempo_field,
			int(textfield_compass_tempo.value)
		)
	)

	current_tempo = 0
	for i in range(textfield_compass_tempo.value):
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
				"Metrónomo",
				size=30,
			),

			ft.Container(
				content=ft.Column(
					[
						tempo_bpm_text,

						tempos_button,
						tempo_list,
						tempo_rows,
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
		("Metrónomo", ft.Icons.TIMER)]

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

		if text == "Metrónomo":
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
