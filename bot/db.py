import json
import os

json_file_path = "data.json"

def load_data():
    try:
        with open(json_file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(db):
    with open(json_file_path, "w") as file:
        json.dump(db, file, indent=2)
