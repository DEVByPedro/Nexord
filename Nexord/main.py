from config.dependencies.Structure import install_dependencies, configure_application

install_dependencies()
configure_application()

from apps.app_configure_structure import app_configure_structure as configure_structure

import flet as ft

def main(page: ft.Page):

	page.title = "Nexord"

	page.padding = 0

	page.window.icon = "nexord.ico"

	page.window.min_width = 1000
	page.window.min_height = 800

	configure_structure.configure_application_structure(page)

	page.window.maximized = True
	page.update()


ft.run(main, assets_dir="assets")
