import flet as ft

from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme, swap_theme
from config.leftbar.LeftBarConfig import get_current_leftbar_state
from content.application.infra.instruments.Instruments import open_instruments
from content.application.infra.tuner.Tuner import open_afinador
from content.application.infra.metronome.Metronome import open_metronome
from content.application.infra.tunings.Tunings import open_tuning

other_page = ft.Container(expand=True)
rota_atual = "afinacoes"

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
		e.data = "hovered_button"
		page.update()

	def leftbar_content():
		global rota_atual

		def update_clicked_button(e, route):
			buttons = content.controls[1]

			change_route(route)

			for button in buttons.controls:
				button_text=button.content.controls[1].value.lower()
				if button_text == route:
					button.data = "hovered_button"
				else:
					button.data = ""
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
			"instrumentos": open_instruments,
			"afinacoes": open_tuning,
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
									ft.Icon(ft.Icons.MENU, data="leftbar_button_icon"),
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
									ft.Icon(ft.Icons.MIC, data="leftbar_button_icon"),
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
									ft.Icon(ft.Icons.TIMER, data="leftbar_button_icon"),
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
						instrumentos := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.COLLECTIONS_BOOKMARK, data="leftbar_button_icon"),
									ft.Text("Meus Instrumentos", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e, button="instrumentos": update_clicked_button(e, button)
						),
						tuning := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.STORAGE, data="leftbar_button_icon"),
									ft.Text("Afinações", visible=False)
								],
								alignment=ft.MainAxisAlignment.START,
								vertical_alignment=ft.CrossAxisAlignment.CENTER,
							),
							style=ft.ButtonStyle(
								shape=ft.RoundedRectangleBorder(radius=5),
								padding=5,
								mouse_cursor=ft.MouseCursor.CLICK,
							),
							on_click=lambda e, button="afinacoes": update_clicked_button(e, button)
						),
						escalas := ft.Button(
							ft.Row(
								[
									ft.Icon(ft.Icons.MUSIC_NOTE, data="leftbar_button_icon"),
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
									ft.Icon(ft.Icons.DARK_MODE, data="leftbar_button_icon"),
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

		set_theme(page, get_current_theme())

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
					data="leftbar",
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
