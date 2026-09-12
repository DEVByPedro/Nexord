from content.application.infra.instruments.InstrumentsConfig import create_instruments_json
from content.application.infra.tuner.afinacoes.Afinacoes import create_afinacoes_json


def install_dependencies():

	import subprocess
	import sys

	try:
		import flet
		import sounddevice as sd
		import numpy as np
		import screeninfo
		import pycaw
	except 	ModuleNotFoundError:
		print()
		print("Installing modules...")
		print()
		subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "sounddevice"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "screeninfo"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "pycaw"])
		print()
		print("Required modules are installed successfully.")
		print()
		print("Starting Nexord!")
		print()

def configure_application():

	from config.leftbar.LeftBarConfig import configure_leftbar_json
	from config.user.microphone.MicrophoneSettings import create_microphones_json
	from config.user.user_preferences.UserConfig import create_user_json

	create_user_json()
	create_microphones_json()
	configure_leftbar_json()
	create_afinacoes_json()
	create_instruments_json()