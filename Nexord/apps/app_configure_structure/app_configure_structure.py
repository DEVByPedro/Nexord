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
rota_atual = "metronomo"

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
					key="tempo_button",
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
		key="card_button",
		style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
		on_click=lambda e: increase_compass_tempo_counting(e, textfield_compass_tempo)
	)
	less_compass_tempo_choose = ft.Button(
		"-",
		key="card_button",
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
		key="card_button",
		on_click=lambda e: remove_counting(choose_tempo_field, BPM),
		height=choose_tempo_field.height,
		style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)})
	)
	more_button = ft.Button(
		"+",
		key="card_button",
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

	content = ft.Container(
		expand=True,
		padding=20,
		content=ft.Container(
			ft.Column(
				[
					ft.Text(
						"Metrónomo",
						size=30,
					),

					ft.Container(
						key="card_container",
						expand=True,
						alignment=ft.Alignment(0, 0),
						content=ft.Column(
							[
								tempo_bpm_text,
								tempos_button,
								tempo_list,
								tempo_rows,
							],
							spacing=20,
							horizontal_alignment=ft.CrossAxisAlignment.CENTER,
							alignment=ft.MainAxisAlignment.CENTER,
							tight=True,
						),
					),

					start_tempo_button,
				],
				expand=True,
				horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			),
			key="card_container",
			padding=30,
			border_radius = 20

		)
	)

	set_theme(page, get_current_theme())
	update_compass_tempo_buttons(int(textfield_compass_tempo.value))

	return content

def open_afinador(page):

	title = ft.Text(
		"Afinador",
		size=30,
	)

	mic_button = ft.Button(
		ft.Row(
			[
				ft.Icon(ft.Icons.MIC),
				ft.Text("Configurar Microfone")
			],
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		),
		style=ft.ButtonStyle(
			mouse_cursor = ft.MouseCursor.CLICK,
			shape=ft.RoundedRectangleBorder(radius=5)
		)
	)

	header_row_container = ft.Container(

		ft.Column(
			[
				ft.Row(
					[
						title,
						mic_button
					],
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
				),
			],

		),
		key="card_container",
		padding=20,
		border_radius=20,
	)

	content = ft.Container(
		expand=True,
		padding=20,
		content=ft.Column(
			[
				header_row_container,
				ft.Container(
					expand=True,
					border_radius=20,
					bgcolor="white",
					alignment=ft.Alignment.CENTER,
					content=ft.Column(
						horizontal_alignment=ft.CrossAxisAlignment.CENTER,
						alignment=ft.MainAxisAlignment.CENTER,
						controls=[
							ft.Icon(
								ft.Icons.MIC,
								size=60,
								color=ft.Colors.BLUE_400,
							),

							ft.Text(
								"Aguardando áudio...",
								size=20,
							),
						],
					),
				),
			],
			expand=True,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		),
	)

	return content

def open_scales(page):
	return ft.Container(
		expand=True,
		padding=20,
		content=ft.Column(
			[
				ft.Text(
					"Minhas Escalas",
					size=30,
				)
			],
			expand=True,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		),
	)

def open_musics(page):
	return ft.Container(
		expand=True,
		padding=20,
		content=ft.Column(
			[
				ft.Text(
					"Minhas Músicas",
					size=30,
				)
			],
			expand=True,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		),
	)

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
		global rota_atual

		def update_clicked_button(e, route):
			buttons = content.controls[1]

			change_route(route)

			for button in buttons.controls:
				button_text=button.content.controls[1].value.lower()
				if button_text == route:
					button.key = "hovered_button"
				else:
					button.key = ""
				set_theme(page, get_current_theme())

		def change_route(route):
			global rota_atual

			if route == "metrónomo":
				route = "metronomo"

			if route not in views:
				return

			rota_atual = route
			switcher.content = views[route](page)
			switcher.update()

		views = {
			"afinador": open_afinador,
			"metronomo": open_metronome,
			"escalas": open_scales,
			"musicas": open_musics
		}

		switcher = ft.AnimatedSwitcher(
			content=views[rota_atual](page),
			transition=ft.AnimatedSwitcherTransition.FADE,
			duration=250,
			reverse_duration=180,
			switch_in_curve=ft.AnimationCurve.EASE_OUT,
			switch_out_curve=ft.AnimationCurve.EASE_IN,
			expand=True,

		)

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
							on_click=lambda e, button="afinador": update_clicked_button(e, button)
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
							on_click=lambda e, button="metrónomo": update_clicked_button(e, button)
						),
						escalas := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.MUSIC_NOTE, key="leftbar_button_icon"),
									ft.Text("Escalas", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e, button="escalas": update_clicked_button(e, button)
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
							on_click=lambda e, button="musicas": update_clicked_button(e, button)
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

		other_page.content = switcher

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
				ft.VerticalDivider(
					width=1,
					thickness=1,
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