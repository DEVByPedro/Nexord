from config.dependencies.Structure import install_dependencies, configure_application

install_dependencies()
configure_application()

from apps.app_configure_structure import app_configure_structure as configure_structure

import flet as ft


def main(page: ft.Page):

	page.title = "Nexord"

	page.padding = 0

	page.window.icon = "nexord.png"

	page.window.width = 1000
	page.window.height = 800

	configure_structure.configure_application_structure(page)


ft.run(main, assets_dir="src/icon")
