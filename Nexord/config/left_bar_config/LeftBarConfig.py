import flet as ft

leftbar_config_path = "config/left_bar_config/LeftBarJSON.json"


def configure_leftbar_json():
	import json

	leftbar_json_data = {
		"isOpen": True
	}

	with open(leftbar_config_path, "w") as user_file:
		json.dump(leftbar_json_data, user_file, indent=4)

def get_current_leftbar_state():
	import json
	import os

	if os.path.exists(leftbar_config_path):
		with open(leftbar_config_path, "r") as user_file:
			leftbar_data = json.load(user_file)

		return leftbar_data["isOpen"]
	else:
		return ""

def change_leftbar_state_json():
	import json
	import os

	if os.path.exists(leftbar_config_path):
		with open(leftbar_config_path, "r") as user_file:
			leftbar_data = json.load(user_file)

	if leftbar_data["isOpen"]:
		leftbar_data["isOpen"] = False
	else:
		leftbar_data["isOpen"] = True

	with open(leftbar_config_path, "w") as user_file:
		json.dump(leftbar_data, user_file, indent=4)

def set_status_leftbar_state_json(status):
	import json
	import os

	if os.path.exists(leftbar_config_path):
		with open(leftbar_config_path, "r") as user_file:
			leftbar_data = json.load(user_file)

		leftbar_data["isOpen"] = status

	with open(leftbar_config_path, "w") as user_file:
		json.dump(leftbar_data, user_file, indent=4)

def get_width_from_leftbar_last_state(page):
	is_leftbar_open = get_current_leftbar_state()
	if is_leftbar_open:
		return page.window.width * 0.20
	if not is_leftbar_open:
		return page.window.width * 0.05

def check_leftbar_last_state(page):

	is_leftbar_open = get_current_leftbar_state()

	if not is_leftbar_open:
		swap_left_bar(page)
		swap_left_bar(page)

	page.update()


def swap_left_bar(page: ft.Page):
	def update_control(control):
		if isinstance(control, ft.Container):
			if control.key == "leftbar":
				if get_current_leftbar_state() == True:
					control.width = page.window.width * 0.05
					if page.window.maximized:
						control.width = page.window.width * 0.0385

				if get_current_leftbar_state() == False:
					control.width = page.window.width * 0.20

				change_leftbar_state_json()

		if isinstance(control, ft.Text):
			if get_current_leftbar_state() == True:
				control.visible = True
			if get_current_leftbar_state() == False:
				control.visible = False

		if hasattr(control, "controls"):
			for child in control.controls:
				update_control(child)

		if hasattr(control, "content") and control.content:
			update_control(control.content)

	for control in page.controls:
		update_control(control)

	page.update()
