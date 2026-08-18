import json
import os

path = "config/user/json/user_json.json"

def save(data):
	import json

	with open(path, "w") as user_file:
		json.dump(data, user_file, indent=4)

def create_user_json():
	if not os.path.exists(path):
		json_data_default = {
			"username": os.getenv("username"),
			"user_icon": "",
			"current_theme": "dark",
			"bpm_cap": 250
		}

		with open(path, "w") as user_file:
			json.dump(json_data_default, user_file, indent=4)

def set_user_current_theme(theme):

	if theme not in ["light", "dark"]:
		raise ValueError("Invalid theme. Use 'light' or 'dark'.")

	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["current_theme"] = theme

		save(user_data)

def set_user_username(name):
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["username"] = name

		save(user_data)

def set_user_user_icon(icon_path):
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["user_icon"] = icon_path

		save(user_data)

def set_bpm_cap(bpm):
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["bpm_cap"] = bpm

		save(user_data)

def get_user_username():
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["username"]
	else:
		return ""

def get_user_user_icon():
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["user_icon"]
	else:
		return ""

def get_user_theme():
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["current_theme"]
	else:
		return ""

def get_bpm_cap():
	import json
	import os

	if os.path.exists(path):
		with open(path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["bpm_cap"]
	else:
		return ""