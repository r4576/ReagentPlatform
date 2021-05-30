import os
import json
from celery import Celery
from pymongo import MongoClient

app = Celery('tasks', broker='pyamqp://guest@localhost//')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_SETTINGS_FILE = os.path.join(os.path.join(ROOT_DIR, '.key'), 'db_settings.json')
db_info = json.loads(open(DATABASE_SETTINGS_FILE).read())

db_database = db_info['altas']['database']
db_host = db_info['altas']['host']
db_username = db_info['altas']['username']
db_password = db_info['altas']['password']
db_collection = 'api_synonym'


@app.task
def createSynonyms(mainName, synonymList, casNo):
    client = MongoClient(db_host)
    database = client.get_database(db_database)
    collection = database.get_collection(db_collection)

    for name in synonymList:
        if not collection.find_one({ "subName" : name }):
            collection.insert_one({
                "mainName" : mainName,
                "subName" : name,
                "casNo" : casNo
            })
