from pymongo import MongoClient
import json


def save(collection, jsonFilePath):
    client = MongoClient("mongodb+srv://next:nextproject@cluster0.myrfh.mongodb.net/ChemDatabase?retryWrites=true&w=majority")
    database = client['ChemDatabase']
    collection = database[collection]

    newData = json.dumps(jsonFilePath)
    collection.insert_many(newData)


if __name__ is "__main__":
    save(collection='api_reagentpropertydata', jsonFilePath='dataset/ReagentPropertyDataset.json')
    save(collection='api_materialsafetydata', jsonFilePath='dataset/MaterialSafetyDataset.json')
