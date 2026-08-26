from pycaw.pycaw import AudioUtilities
from pycaw.constants import EDataFlow, DEVICE_STATE

import sounddevice as sd
import json
import os

path = "config/user/json/micriphones.json"

def save(data):
    import json

    with open(path, "w") as user_file:
        json.dump(data, user_file, indent=4)

def create_microphones_json():
    if not os.path.exists(path):
        json_microphones = {
            "all_microphones": get_microphones(),
            "default_microphone": ""
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)

        save(json_microphones)

def save_microphones(default_mic):
    json_microphones = {
        "all_microphones": get_microphones(),
        "default_microphone": default_mic
    }

    save(json_microphones)

def get_saved_microphones():
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_microphones():
    devices = AudioUtilities.GetAllDevices(
        data_flow=EDataFlow.eCapture.value,
        device_state=DEVICE_STATE.ACTIVE.value
    )

    microphones = []

    for index, device in enumerate(devices):
        microphones.append({
            "index": index + 1,
            "id": device.id,
            "name": device.FriendlyName
        })

    return microphones

def get_default_microphone():
    return get_saved_microphones()["default_microphone"]

def isDefaultMicrophoneConfigurated():
    return True if get_saved_microphones()["default_microphone"] != "" else False