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
            "instrumento_quantidade_cordas": int(strings)
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
        for i , obj in enumerate(favorite_instruments):
            if obj == index:
                favorite_instruments.pop(i)

    new_favorite_list = []
    for index_favorite in favorite_instruments:
        if index_favorite >= index:
            index_favorite = int(index_favorite - 1)
        new_favorite_list.append(index_favorite)

    data["instrumentos_favoritos"] = new_favorite_list

    save(data)

def get_instrument_name_by_index(index):
    if index == None: return ""
    return instruments_json()["instrumentos"][index - 1]["instrumento_nome"]

def get_description_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_descricao"]

def get_brand_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_marca"]

def get_strings_name_by_index(index):
    return instruments_json()["instrumentos"][index - 1]["instrumento_quantidade_cordas"]

def edit_instrument_json(index, name, description, brand, strings):

    data = instruments_json()

    instrument = data["instrumentos"][index-1]

    instrument["instrumento_nome"] = name
    instrument["instrumento_descricao"] = description
    instrument["instrumento_marca"] = brand
    instrument["instrumentos_quantidades_cordas"] = strings

    save(data)

def get_instruments_name_strings():

    all_instruments = get_all_instruments()

    list = []
    for instrument in all_instruments:
        list.append({"nome": instrument["instrumento_nome"], "cordas": instrument["instrumento_quantidade_cordas"]})

    return list

def get_strings_by_name(name):

    for instrument in get_all_instruments():
        if instrument["instrumento_nome"] == name:
            return instrument["instrumento_quantidade_cordas"]

def get_instrument_index_by_name(name):

    data = instruments_json()

    for instrument in data["instrumentos"]:
        if instrument["instrumento_nome"] == name:
            return instrument["index"]

    return None

