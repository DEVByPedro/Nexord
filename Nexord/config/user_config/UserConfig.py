def save(path, data):
	import json

	with open(path, "w") as user_file:
		json.dump(data, user_file, indent=4)

def configure_user_json():
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	default_user_data = {
		"username": os.getenv("username"),
		"user_icon": "",
		"current_theme": "dark",
		"bpm_cap": 300
	}

	with open(user_config_path, "w") as user_file:
		json.dump(default_user_data, user_file, indent=4)

def set_user_current_theme(theme):

	if theme not in ["light", "dark"]:
		raise ValueError("Invalid theme. Use 'light' or 'dark'.")

	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["current_theme"] = theme

		save(user_config_path, user_data)

def set_user_username(name):
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["username"] = name

		save(user_config_path, user_data)

def set_user_user_icon(icon_path):
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["user_icon"] = icon_path

		save(user_config_path, user_data)

def set_bpm_cap(bpm):
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		user_data["bpm_cap"] = bpm

		save(user_config_path, user_data)

def get_user_username():
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["username"]
	else:
		return ""

def get_user_user_icon():
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["user_icon"]
	else:
		return ""

def get_bpm_cap():
	import json
	import os

	user_config_path = "config/user_config/user_json.json"

	if os.path.exists(user_config_path):
		with open(user_config_path, "r") as user_file:
			user_data = json.load(user_file)

		return user_data["bpm_cap"]
	else:
		return ""