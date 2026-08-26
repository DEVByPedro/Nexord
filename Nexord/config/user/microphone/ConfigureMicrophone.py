import json
import os

path = "config/user/json/microphones.json"

def save(data):
    import json

    with open(path, "w") as user_file:
        json.dump(data, user_file, indent=4)

def create_user_json():
    if not os.path.exists(path):
        json_data_default = {
            "all_microphones": os.getenv("username"),
            "selected_microphone": ""
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)

        save(json_data_default)