from pymongo import MongoClient
import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_SETTINGS_FILE = os.path.join(os.path.join(ROOT_DIR, '.key'), 'db_settings.json')

def save(collection, jsonFilePath, keyFilePath=None):
    db_info = json.loads(open(DATABASE_SETTINGS_FILE).read())
    client = MongoClient(db_info['altas']['host'])
    database = client[db_info['altas']['database']]
    collection = database[collection]

    newData = []
    with open(jsonFilePath, 'r', encoding='utf-8') as json_file:
        newData = json.load(json_file)
    
    if keyFilePath is not None:
        keys_json = None
        with open(keyFilePath, 'r', encoding='utf-8') as json_file:
            keys_json = json.load(json_file)

        for data in newData:
            for key, value in keys_json.items():
                data[value] = data.pop(key)
    
    # collection.insert_many(newData)


if __name__ == "__main__":
    # save(collection='api_reagentpropertydata', jsonFilePath='dataset/ReagentPropertyData.json')
    save(collection='api_materialsafetydata', jsonFilePath='dataset/material_safety_data.json', keyFilePath='dataset/material_safety_column.json')
