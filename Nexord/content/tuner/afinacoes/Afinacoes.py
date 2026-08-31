import json
import os

path = "config/user/json/afinacoes.json"

def save(user_data):
    with open(path, "w") as file:
        json.dump(user_data, file, indent=4)

def afinacao_json():
    with open(path, "r") as file:
        return json.load(file)

def create_afinacoes_json():
    if not os.path.exists(path):
        json_afinacao = {
            "afinacoes": [
                {
                    "index": 1,
                    "afinacao_descricao": "Afinação Padrão",
                    "notas": [
                        ("E", 82.41),
                        ("A", 110.00),
                        ("D", 146.83),
                        ("G", 196.00),
                        ("B", 246.94),
                        ("E", 329.63),
                    ]
                }
            ],
            "afinacao_atual": 1
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)

        save(json_afinacao)

def get_current_afinacao():

    json_data = afinacao_json()

    current_tuning_index = json_data["afinacao_atual"]

    for tuning in json_data["afinacoes"]:
        if tuning["index"] == current_tuning_index:

            return tuning["notas"]

    return None

def get_current_tuning_description():
    json_data = afinacao_json()

    afinacao_atual_index = json_data["afinacao_atual"] - 1

    return json_data["afinacoes"][afinacao_atual_index]["afinacao_descricao"]

def get_all_tuning_saved():

    return afinacao_json()["afinacoes"]

def get_current_tuning_notes():

    json_data = afinacao_json()

    afinacao_atual_index = json_data["afinacao_atual"] - 1

    afinacoes = json_data["afinacoes"][afinacao_atual_index]["notas"]

    notes = ""

    for i, (note, frequency) in enumerate(afinacoes):
        if i < len(afinacoes):
            notes += note + " "
        else:
            notes += note

    return notes

def get_current_tuning_notes_frequency():
    json_data = afinacao_json()

    afinacao_atual_index = json_data["afinacao_atual"] - 1

    return json_data["afinacoes"][afinacao_atual_index]["notas"]

def set_current_default_tuning(index):

    json_data = afinacao_json()

    json_data["afinacao_atual"] = index

    save(json_data)

def insert_tuning(description, notes):
    json_data = afinacao_json()

    next_index = len(json_data["afinacoes"]) + 1

    json_data["afinacoes"].append(
        {
            "index": next_index,
            "afinacao_descricao": description,
            "notas": notes
        }
    )

    save(json_data)

def delete_tuning_json(index):
    json_data = afinacao_json()

    if index > 0:
        for tuning in json_data["afinacoes"]:
            if tuning["index"] == index:
                json_data["afinacoes"].pop(index)

        if tuning["index"] > index:
            tuning["index"] -= 1

    save(json_data)

def get_current_default_tuning():
    return afinacao_json()["afinacao_atual"]

def get_tuning_description_by_index(index):
    json_data = afinacao_json()

    return json_data["afinacoes"][index]["afinacao_descricao"]