from apps.app_change_theme.app_change_theme import set_theme, get_current_theme
from config.user_config.UserConfig import configure_user_json
from config.left_bar_config.LeftBarConfig import configure_leftbar_json, check_leftbar_last_state

def get_imports():
	try:
		import flet as ft
		import sounddevice as sd
		import numpy as np
		import screeninfo
		import json
		import socket
	except ModuleNotFoundError:
		print("Required modules are not installed. Initiallizing installation of the required modules...")
		print()
		import subprocess
		subprocess.check_call(["python", "-m", "pip", "install", "flet", "sounddevice", "numpy", "screeninfo"])
		print()
		print("Required modules are installed successfully.")
		print()

def check_theme(page):
	set_theme(page, get_current_theme())

def create_jsons():
	import os

	user_json_path = "config/user_config/user_json.json"
	leftbar_json_path = "config/left_bar_config/LeftBarJSON.json"

	if not os.path.exists(user_json_path):
		configure_user_json()
	elif not os.path.exists(leftbar_json_path):
		configure_leftbar_json()

def configure_window_size(page):

	from screeninfo import get_monitors

	default_monitor = next(
		(monitor for monitor in get_monitors() if monitor.is_primary)
	)

	page.window.width = default_monitor.width / 1.3
	page.window.height = default_monitor.height / 1.3

	page.window.left = 0
	page.window.top = 0

	page.update()

def apply_colors(page):
	check_theme(page)

def customize_app(page):
	configure_window_size(page)
	check_leftbar_last_state(page)

def initialize_setup():
	get_imports()
	create_jsons()