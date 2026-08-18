import asyncio
import threading
from time import sleep

import flet as ft

from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme, swap_theme, get_current_textcolor
from config.leftbar.LeftBarConfig import get_current_leftbar_state, configure_leftbar_json, \
	set_status_leftbar_state_json, swap_left_bar
from config.user.user_preferences.UserConfig import get_bpm_cap

other_page = ft.Container(expand=True)
metronome_running = False

# ARRUMAR OS TEMPO_BUTTON E O BOTÂO DE INICIAR TEMPO
def open_metronome(page):
	global metronome_running
	global other_page

	def verify_tempo(e, bpm):
		try:
			field = e.control

			value = "".join(char for char in field.value if char.isdigit())

			if value == "":
				value = "1"

			if int(value) > get_bpm_cap():
				value = str(get_bpm_cap())

			field.value = value
			field.update()

			tempo_bpm_text.value = f"{value} BPM"
			tempo_bpm_text.update()
		except Exception:
			pass

	def elevate_counting(textfield: ft.TextField, bpm):
		value = int(textfield.value or 0)

		if 1 <= value < get_bpm_cap():
			value += 1
			textfield.value = str(value)
			tempo_bpm_text.value = f"{value} BPM"
			tempo_bpm_text.update()

		textfield.update()

	def remove_counting(textfield: ft.TextField, bpm):
		value = int(textfield.value or 0)

		if value > 1:
			value -= 1
			textfield.value = str(value)
			tempo_bpm_text.value = f"{value} BPM"
			tempo_bpm_text.update()

		textfield.update()

	def increase_compass_tempo_counting(e, textfield):
		value = int(textfield.value or 0)

		if 0 < value < 12:
			value += 1

		textfield.value = str(value)
		textfield.update()
		update_compass_tempo_buttons(value)

	def decrease_compass_tempo_counting(e, textfield):
		value = int(textfield.value or 0)

		if value > 1:
			value -= 1

		textfield.value = str(value)
		textfield.update()
		update_compass_tempo_buttons(value)

	def play_click():
		import sounddevice as sd
		import numpy as np

		sample_rate = 44100
		duration = 0.05
		frequency = 1000

		t = np.linspace(0, duration, int(sample_rate * duration), False)
		sound = 0.3 * np.sin(2 * np.pi * frequency * t)

		sd.play(sound, sample_rate, blocking=False)

	def play_strong_click():
		import sounddevice as sd
		import numpy as np

		sample_rate = 44100
		duration = 0.07
		frequency = 1500
		volume = 0.8

		t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
		sound = np.sin(2 * np.pi * frequency * t)
		envelope = np.exp(-t * 60)
		sound = sound * envelope * volume

		sd.play(sound.astype(np.float32), sample_rate, blocking=False)

	def only_numbers(e):
		try:
			value = "".join(c for c in e.control.value if c.isdigit())

			if value == "":
				value = "1"

			if int(value) > 12:
				value = "12"

			if e.control.value != value:
				e.control.value = value
				e.control.update()

			update_compass_tempo_buttons(int(value))
		except ValueError:
			pass

	def update_compass_tempo_buttons(current_tempo=None):

		global metronome_running

		if current_tempo is None:
			current_tempo = int(textfield_compass_tempo.value or 1)

		tempos_button.controls.clear()

		for i in range(current_tempo):
			tempos_button.controls.append(
				ft.Container(
					width=10,
					height=10,
					border_radius=50,
				)
			)

		theme = get_current_theme()
		color = get_current_textcolor(theme)

		for button in tempos_button.controls:
			button.bgcolor = color

		metronome_running = False
		start_tempo_button.text = "Começar Metrónomo"

		page.update()

	async def run_metronome(button, bpm_field, tempo):
		global metronome_running

		current_index = 0

		while metronome_running:
			try:
				bpm = int(bpm_field.value)
			except (ValueError, TypeError):
				bpm = 120

			interval = 60 / bpm

			# Atualiza as cores
			normal_color = get_current_textcolor(get_current_theme())

			if get_current_theme() == "dark":
				active_color = "#818cf8"
			else:
				active_color = "#16a34a"

			for i, tempo_button in enumerate(tempos_button.controls):
				tempo_button.bgcolor = (
					active_color
					if i == current_index
					else normal_color
				)

			# Atualiza a interface
			page.update()

			# Toca o click
			if current_index == 0:
				play_strong_click()
			else:
				play_click()

			# Espera sem bloquear o Flet
			await asyncio.sleep(interval)

			current_index += 1

			if current_index >= tempo:
				current_index = 0

		normal_color = get_current_textcolor(get_current_theme())

		for tempo_button in tempos_button.controls:
			tempo_button.bgcolor = normal_color

		button.content = "Começar Metrónomo"
		page.update()

	def start_tempo(button, bpm_field, tempo):
		global metronome_running

		if not metronome_running:
			metronome_running = True
			button.content = "Parar Metrónomo"
			page.update()

			page.run_task(
				run_metronome,
				button,
				bpm_field,
				tempo
			)

		else:
			metronome_running = False
			button.content = "Começar Metrónomo"
			page.update()

	metronome_running = False

	last_state = get_current_leftbar_state()
	if last_state == True:
		swap_left_bar(page)

	BPM = 120
	tempos_button = ft.Row(
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		tight=True,
		spacing=10
	)

	textfield_compass_tempo = ft.TextField(
		hint_text="Max 12",
		width=100,
		value="4",
		on_change=lambda e: only_numbers(e)
	)

	more_compass_tempo_choose = ft.Button(
		"+",
		style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
		on_click=lambda e: increase_compass_tempo_counting(e, textfield_compass_tempo)
	)
	less_compass_tempo_choose = ft.Button(
		"-",
		style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
		on_click=lambda e: decrease_compass_tempo_counting(e, textfield_compass_tempo)
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
	choose_tempo_field = ft.TextField(width=100, value=str(BPM), on_change=lambda e: verify_tempo(e, BPM))
	less_button = ft.Button(
		"-",
		on_click=lambda e: remove_counting(choose_tempo_field, BPM),
		height=choose_tempo_field.height,
		style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	)
	more_button = ft.Button(
		"+",
		on_click=lambda e: elevate_counting(choose_tempo_field, BPM),
		height=choose_tempo_field.height,
		style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	)

	tempo_rows = ft.Column(
		[
			ft.Text(
				"Batidas por Minuto:",
				size=15,
				weight=ft.FontWeight.W_500,
				text_align=ft.TextAlign.CENTER
			),
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

	current_tempo = 0

	start_tempo_button = ft.Button(
		"Começar Metrónomo",
		style=ft.ButtonStyle(
			shape={"": ft.RoundedRectangleBorder(radius=5)},
			padding=15
		),
		on_click=lambda e: start_tempo(
			start_tempo_button,
			choose_tempo_field,
			int(textfield_compass_tempo.value)
		)
	)

	for i in range(int(textfield_compass_tempo.value)):
		tempos_button.controls.append(
			ft.Container(
				width=10,
				height=10,
				border_radius=50
			)
		)

	other_page.content = ft.Column(
		[
			ft.Container(),
			ft.Text("Metrónomo", size=30),
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
	update_compass_tempo_buttons(int(textfield_compass_tempo.value))
	page.update()

def configure_window(page: ft.Page):
	def configure_leftbar_content(leftbar):
		buttons = leftbar.content.controls

		for i in range(len(buttons)):
			for j in range(len(buttons[i].controls)):
				text = buttons[i].controls[j].content.controls[1]

				text.visible = True if get_current_leftbar_state() else False

	def animate_leftbar(e, leftbar):
		leftbar.width = 300 if leftbar.width == 50 else 50
		buttons = leftbar.content.controls

		for i in range(len(buttons)):
			for j in range(len(buttons[i].controls)):
				text = buttons[i].controls[j].content.controls[1]

				text.visible = True if text.visible == False else False

		leftbar.update()

	def hover_button(e):
		e.key = "hovered_button"
		page.update()

	def leftbar_content():
		content = ft.Column(
			[
				# Top Buttons
				ft.Column(
					[
						top_button := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.MENU, key="leftbar_button_icon"),
									ft.Text("Menu", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e: animate_leftbar(e, leftbar),
							on_hover=hover_button,
						)
					],
					horizontal_alignment=ft.CrossAxisAlignment.STRETCH
				),

				# Middle Buttons
				ft.Column(
					[
						afinador := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.MIC, key="leftbar_button_icon"),
									ft.Text("Afinador", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
						),
						metronomo := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.TIMER, key="leftbar_button_icon"),
									ft.Text("Metrónomo", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e: open_metronome(page)
						),
						escalas := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.MUSIC_NOTE, key="leftbar_button_icon"),
									ft.Text("Escala", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
						),
						musicas := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.LIBRARY_MUSIC),
									ft.Text("Musicas", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5
							),
						)
					],
					horizontal_alignment=ft.CrossAxisAlignment.STRETCH
				),

				# Bottom Buttons
				ft.Column(
					[
						tema := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.DARK_MODE, key="leftbar_button_icon"),
									ft.Text("Mudar Tema", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e: swap_theme(page)
						),
						user := ft.Button(
							ft.Row(
								[
									ft.CircleAvatar(
										foreground_image_src="config/user/src/icon.png",
										radius=10,
									),
									ft.Text("Perfil", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
						)
					],
					horizontal_alignment=ft.CrossAxisAlignment.STRETCH
				)
			],
			horizontal_alignment=ft.CrossAxisAlignment.START,
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			expand=True
		)

		return content

	def resize(e):
		if get_current_leftbar_state():
			leftbar.width = 300
		else:
			leftbar.width = 50

	page.on_resize = resize

	page.add(
		ft.Row(
			[
				leftbar := ft.Container(
					key="leftbar",
					content=leftbar_content(),
					padding=10,
					width=50,
					animate=ft.Animation(
						duration=300,
						curve=ft.AnimationCurve.FAST_OUT_SLOWIN
					)
				),
				other_page
			],
			expand=True,
			spacing=0
		)
	)

	configure_leftbar_content(leftbar)

def configure_application_structure(page: ft.Page):
	configure_window(page)
	set_theme(page, get_current_theme())
	configure_leftbar_json()