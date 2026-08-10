from assets.application_css.configure_application_css.configure_application_css import configure_application_css
from apps.app_setup_window.app_setup_window import initialize_setup, customize_app, apply_colors

initialize_setup()

import flet as ft

def main(page: ft.Page):

	# Customization
	page.title = "Nexord"
	page.window.icon = "icon.ico"
	page.padding = 0

	customize_app(page)
	configure_application_css(page)
	apply_colors(page)

	page.update()

ft.app(main, assets_dir="assets/src")