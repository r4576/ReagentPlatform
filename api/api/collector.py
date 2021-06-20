from django.conf import settings
from contents.reagent_property_data_Pubchem import get_query, get_Table_data

from rest_framework import status
from pymongo import MongoClient
from datetime import datetime

import requests

client = MongoClient(settings.DB_HOST)
database = client.get_database(settings.DB_DATABASE)
collections = settings.DB_COLLECTIONS

DB_SERVER = settings.dbServer


class Collector:
    def __init__(self):
        self.__data = { 
            'Keyword' : None,
            'CasNo' : None,
            'Name' : None,
            'ReagentProperty' : None,
            'MaterialSafety' : None
        }

    def execute(self, keyword):
        self.__initializeData()

        self.__data['Keyword'] = keyword

        self.__setCasNoMainName()
        self.__setReagentProperty()
        self.__setMaterialSafety()

        return self.__data

    def __initializeData(self):
        self.__data['Keyword'] = None
        self.__data['CasNo'] = None
        self.__data['Name'] = None
        self.__data['ReagentProperty'] = None
        self.__data['MaterialSafety'] = None

    def __setCasNoMainName(self):
        collection = database.get_collection(collections['Synonym'])
        query = collection.find_one({'subName':self.__data['Keyword']})
        if query:
            print("[ /api/search?keyword={} ] {} {} Synonym Data from Database HTTP_200_OK".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
            self.__data['CasNo'] = query['casNo']
            self.__data['Name']  = query['mainName']
        else:
            print("[ /api/search?keyword={} ] {} No Synonym Data from Database HTTP_404_NotFound".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__setCasNoMainNameFromPubChem(self.__data['Keyword'])

    def __setCasNoMainNameFromPubChem(self, keyword):
        print("[ /api/search?keyword={} ] {} Get Synonym Data from PubChem".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        synonym = get_query(keyword)
        if synonym:
            print("[ /api/search?keyword={} ] {} Synonym Data from PubChem HTTP_200_OK".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__data['CasNo'] = synonym['casNo']
            self.__data['Name'] = synonym['name']
            self.__sendSynonymDataToDBMS(synonym)
        else:
            print("[ /api/search?keyword={} ] {} No Synonym Data from PubChem HTTP_404_NotFound".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))           

    def __sendSynonymDataToDBMS(self, data):
        requests.post(DB_SERVER + "/create/synonym", data=data)

    def __setReagentProperty(self):
        collection = database.get_collection(collections['Reagent Property'])
        query = collection.find_one({'casNo':self.__data['CasNo']})
        if query:
            print("[ /api/search?keyword={} ] {} {} Reagent property Data from Database HTTP_200_OK".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
            self.__data['ReagentProperty'] = { 'casNo' : query['casNo'],
                                               'formula' : query['formula'],
                                               'molecularWeight' : query['molecularWeight'],
                                               'meltingpoint' : query['meltingpoint'],
                                               'boilingpoint' : query['boilingpoint'],
                                               'density' : query['density'] }
        else:
            print("[ /api/search?keyword={} ] {} No Reagent property Data from Database HTTP_404_NotFound".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__setReagentPropertyFromPubChem(self.__data['Keyword'])
         
    def __setReagentPropertyFromPubChem(self, keyword):
        print("[ /api/search?keyword={} ] {} Get Reagent Property Data from PubChem".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        reagent = get_Table_data(keyword)
        if reagent:
            print("[ /api/search?keyword={} ] {} Reagent property Data from PubChem HTTP_200_OK".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__data['ReagentProperty'] = reagent
            self.__sendReagentDataToDBMS(reagent)
        else:
            print("[ /api/search?keyword={} ] {} No Reagent Property Data from PubcheC HTTP_404_NotFound".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
 
    def __sendReagentDataToDBMS(self, data):
        requests.post(DB_SERVER + "/create/reagent", data=data)
  
    def __setMaterialSafety(self):
        collection = database.get_collection(collections['Material Safety'])
        query = collection.find_one({'casNo':self.__data['CasNo']})
        if query:
            print("[ /api/search?keyword={} ] {} {} Material Safety Data from Database HTTP_200_OK".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
            self.__data['MaterialSafety'] = { 'casNo' : query['casNo'],                     'phyStatus' : query['phyStatus'],               'phyColor' : query['phyColor'],
                                              'phySmell' : query['phySmell'],               'phyTaste' : query['phyTaste'],                 'NFPAHealthNum'  : query['NFPAHealthNum'],
                                              'NFPAFireNum'  : query['NFPAFireNum'],        'NFPAReactionNum'  : query['NFPAReactionNum'],  'NFPASpecialNum'  : query['NFPASpecialNum'],
                                              'NFPAHealth' : query['NFPAHealth'],           'NFPAFire' : query['NFPAFire'],                 'NFPAReaction' : query['NFPAReaction'],
                                              'NFPASpecial' : query['NFPASpecial'],         'safReaction' : query['safReaction'],           'safCorrosion' : query['safCorrosion'],
                                              'safAvoid' : query['safAvoid'],               'humNormal' : query['humNormal'],               'humInhale' : query['humInhale'],
                                              'humSkin' : query['humSkin'],                 'humEye' : query['humEye'],                     'humMouth' : query['humMouth'],
                                              'humEtc' : query['humEtc'],                   'emeInhale' : query['emeInhale'],               'emeSkin' : query['emeSkin'],
                                              'emeEye' : query['emeEye'],                   'emeMouth' : query['emeMouth'],                 'emeEtc' : query['emeEtc'],
                                              'accLeakage' : query['accLeakage'],           'accFire' : query['accFire'],                   'treStorage' : query['treStorage'],
                                              'treTreatcaution' : query['treTreatcaution'], 'treDisposal' : query['treDisposal'], }
        else:
            print("[ /api/search?keyword={} ] {} No Material Safety Data from Database HTTP_404_NotFound".format(self.__data['Keyword'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
