import platform
import subprocess
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
    if platform.system() == "Windows":
        return get_microphones_windows()

    elif platform.system() == "Linux":
        return get_microphones_linux()

    return []

def get_microphones_windows():
    from pycaw.pycaw import AudioUtilities
    from pycaw.constants import EDataFlow, DEVICE_STATE

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

def get_microphones_linux():
    result = subprocess.run(
        ["pactl", "list", "sources"],
        capture_output=True,
        text=True,
        check=True
    )

    microphones = []

    current_id = None
    current_name = None
    current_media_class = None

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("Name:") or line.startswith("Nome:"):
            current_id = line.split(":", 1)[1].strip()

        elif line.startswith("Description:") or line.startswith("Descrição:"):
            current_name = line.split(":", 1)[1].strip()

        elif line.startswith("media.class"):
            current_media_class = line.split("=", 1)[1].strip().strip('"')

        elif line.startswith("State:") or line.startswith("Estado:"):

            if (
                    current_id
                    and current_name
                    and current_media_class == "Audio/Source"
            ):
                microphones.append({
                    "index": len(microphones) + 1,
                    "id": current_id,
                    "name": current_name
                })

            current_id = None
            current_name = None
            current_media_class = None

    return microphones

def get_default_microphone():
    return get_saved_microphones()["default_microphone"]

def isDefaultMicrophoneConfigurated():
    return True if get_saved_microphones()["default_microphone"] != "" else False