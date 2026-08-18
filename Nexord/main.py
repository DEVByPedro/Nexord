from config.dependencies.Structure import configure_application
from apps.app_configure_structure import app_configure_structure as configure_structure

configure_application()

import flet as ft

def main(page: ft.Page):
	page.window.title = "Nexord"

	page.padding = 0

	page.window.width = 1000
	page.window.height = 800

	configure_structure.configure_application_structure(page)


ft.run(main)