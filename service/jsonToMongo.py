from pymongo import MongoClient
import json


def save(collection, jsonFilePath, keyFilePath=None):
    client = MongoClient("mongodb+srv://next:nextproject@cluster0.myrfh.mongodb.net/ChemDatabase?retryWrites=true&w=majority")
    database = client['ChemDatabase']
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
    
    collection.insert_many(newData)


if __name__ == "__main__":
    # save(collection='api_reagentpropertydata', jsonFilePath='dataset/ReagentPropertyData.json')
    save(collection='api_materialsafetydata', jsonFilePath='dataset/material_safety_data.json', keyFilePath='dataset/material_safety_column.json')
