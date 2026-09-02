import json
import os

path = "config/user/json/instruments.json"

def save(user_data):
    with open(path, "w") as file:
        json.dump(user_data, file, indent=4)

def instruments_json():
    with open(path, "r") as file:
        return json.load(file)

def create_instruments_json():
    if not os.path.exists(path):
        json_afinacao = {
            "instrumentos": [],
            "instrumentos_favoritos": []
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)

        save(json_afinacao)

def insert_new_instrument(name, description, brand, strings):

    data = instruments_json()

    index = len(data["instrumentos"]) + 1
    data["instrumentos"].append(
        {
            "index": index,
            "instrumento_nome": name,
            "instrumento_descricao": description,
            "instrumento_marca": brand,
            "instrumentos_quantidades_cordas": int(strings)
        }
    )

    save(data)

def get_all_instruments():
    return instruments_json()["instrumentos"]

def get_all_favorite_instruments():
    return instruments_json()["instrumentos_favoritos"]

def favorite_instrument_json(index):

    data = instruments_json()

    data["instrumentos_favoritos"].append(index)

    save(data)

def unfavorite_instrument_json(index):

    data = instruments_json()

    for index_ in data["instrumentos_favoritos"]:
        if index_ == index:
            data["instrumentos_favoritos"].remove(index_)

    save(data)

def get_instrument_by_index(index):
    return instruments_json()["instrumentos"][index - 1]

def delete_instrument_json(index):
    data = instruments_json()

    all_instruments = data["instrumentos"]
    all_instruments.pop(index - 1)

    for instrument in all_instruments:
        if instrument["index"] > index:
            instrument["index"] -= 1

    favorite_instruments = data["instrumentos_favoritos"]
    if index in favorite_instruments:
        favorite_instruments.pop(index - 1)

    new_favorite_list = []
    for index_favorite in favorite_instruments:
        if index_favorite >= index:
            index_favorite = int(index_favorite - 1)
        new_favorite_list.append(index_favorite)

    data["instrumentos_favoritos"] = new_favorite_list

    save(data)

def get_instrument_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_nome"]

def get_description_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_descricao"]

def get_brand_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_marca"]

def get_strings_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumentos_quantidades_cordas"]

def edit_instrument_json(index, name, description, brand, strings):

    data = instruments_json()

    instrument = data["instrumentos"][index-1]

    instrument["instrumento_nome"] = name
    instrument["instrumento_descricao"] = description
    instrument["instrumento_marca"] = brand
    instrument["instrumentos_quantidades_cordas"] = strings

    save(data)
