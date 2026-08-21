from config.user.user_preferences.UserConfig import create_user_json

import subprocess
import sys

def install_dependencies():
	try:
		import flet
		import sounddevice as sd
		import numpy as np
		import screeninfo
	except 	ModuleNotFoundError:
		print()
		print("Installing modules...")
		print()
		subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "sounddevice"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "screeninfo"])
		print()
		print("Required modules are installed successfully.")
		print()


def configure_application():
	install_dependencies()
	create_user_json()