from config.user.user_preferences.UserConfig import create_user_json

def install_dependencies():
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

def configure_application():
	install_dependencies()
	create_user_json()