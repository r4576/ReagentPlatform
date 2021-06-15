from django.conf import settings
from content.reagent_property_data_Pubchem import get_query, get_Table_data

from rest_framework import response, status
from pymongo import MongoClient
from datetime import datetime

import requests

client = MongoClient(settings.DB_HOST)
database = client.get_database(settings.DB_DATABASE)

class Collector:
    def __init__(self):
        self.__data = { 
            'Keyword' : None,
            'Name' : None,
            'ReagentProperty' : None,
            'MaterialSafety' : None
        }

        self.__keyword = None
        self.__casNo = None

        self.__pubchemData = { 
            'ReagentProperty' : { 
                'Status'   : None,
                'Contents' : { } 
            },
            'Synonym' : { 
                'Status'   : None,
                'Contents' : [ ] 
            }
        }
        
    def initializeData(self):
        self.__data['Keyword'] = None
        self.__data['Name'] = None
        self.__data['ReagentProperty'] = None
        self.__data['MaterialSafety'] = None

        self.__keyword = None
        self.__casNo = None

        self.__pubchemData['ReagentProperty']['Status'] = None
        self.__pubchemData['Synonym']['Status'] = None

    @property
    def data(self):
        return self.__data
        
    @data.setter
    def data(self, keyword):
        self.__keyword = keyword
        self.__setNameCasNo()
        self.__setReagentProperty()
        self.__setMaterialSafety()

    def execute(self, keyword):
        self.initializeData()
        self.data = keyword

    def __setNameCasNo(self):
        self.__data['Keyword'] = self.__keyword

        collection = database.get_collection('api_synonym')
        query = collection.find_one({'subName':self.__keyword})
        if query:
            print("[ /api/search?keyword={} ] {} {} Synonym Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
            self.__casNo = query['casNo']
            self.__data['Name'] = query['mainName']
        else:
            print("[ /api/search?keyword={} ] {} No Synonym Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__getSynonymDataFromPubchem()
            if self.__pubchemData['Synonym']['Status'] == status.HTTP_200_OK:
                print("[ /api/search?keyword={} ] {} Synonym Data from Pubchem HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                self.__casNo = self.__pubchemData['ReagentProperty']['Contents']['casNo']
                self.__data['name'] = self.__pubchemData['ReagentProperty']['Contents']['name']
                self.__sendSynonymDataToDBMS(self.__casNo, self.__pubchemData['Synonym']['Contents'])
            elif self.__pubchemData['Synonym']['Status'] == status.HTTP_404_NOT_FOUND:
                print("[ /api/search?keyword={} ] {} No Synonym Data from Pubchem HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                print("[ /api/search?keyword={} ] {} HTTP_500_InternalServerError".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
    def __setReagentProperty(self):
        collections = database.get_collection('api_reagentpropertydata')
        query = collections.find_one({'casNo':self.__casNo})
        if query:
            print("[ /api/search?keyword={} ] {} {} Reagent property Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
            self.__data['ReagentProperty'] = { 'casNo' : query['casNo'],
                                               'formula' : query['formula'],
                                               'molecularWeight' : query['molecularWeight'],
                                               'meltingpoint' : query['meltingpoint'],
                                               'boilingpoint' : query['boilingpoint'],
                                               'density' : query['density'] }
            self.__sendReagentDataToDBMS(self.__data['ReagentProperty'])
        else:
            print("[ /api/search?keyword={} ] {} No Reagent property Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__getReagentDataFromPubchem()
            if self.__pubchemData['ReagentProperty']['Status'] == status.HTTP_200_OK:
                print("[ /api/search?keyword={} ] {} {} Reagent property Data from PubChem HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
                self.__data['ReagentProperty'] = { 'casNo' : self.__pubchemData['ReagentProperty']['Contents']['casNo'],
                                                   'formula' : self.__pubchemData['ReagentProperty']['Contents']['formula'],
                                                   'molecularWeight' : self.__pubchemData['ReagentProperty']['Contents']['molecularWeight'],
                                                   'meltingpoint' : self.__pubchemData['ReagentProperty']['Contents']['meltingpoint'],
                                                   'boilingpoint' : self.__pubchemData['ReagentProperty']['Contents']['boilingpoint'],
                                                   'density' : self.__pubchemData['ReagentProperty']['Contents']['density'] }
                self.__sendReagentDataToDBMS(self.__data['ReagentProperty'])
            elif self.__pubchemData['ReagentProperty']['Status'] == status.HTTP_404_NOT_FOUND:
                print("[ /api/search?keyword={} ] {} No Reagent Property Data from Pubchem HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                print("[ /api/search?keyword={} ] {} HTTP_500_InternalServerError".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def __setMaterialSafety(self):
        collections = database.get_collection('api_materialsafetydata')
        query = collections.find_one({'casNo':self.__casNo})
        if query:
            print("[ /api/search?keyword={} ] {} {} Material Safety Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query['_id']))
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
            print("[ /api/search?keyword={} ] {} No Material Safety Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def __getSynonymDataFromPubchem(self):
        if self.__pubchemData['Synonym']['Status'] is None:
            print("[ /api/search?keyword={} ] {} Get Synonym Data from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            synonym = get_query(self.__keyword)
            if synonym:
                self.__pubchemData['Synonym']['Status'] = status.HTTP_200_OK
                self.__pubchemData['Synonym']['Contents'] = synonym
            else:
                self.__pubchemData['Synonym']['Status'] = status.HTTP_404_NOT_FOUND            

    def __getReagentDataFromPubchem(self):
        if self.__pubchemData['ReagentProperty']['Status'] is None:
            print("[ /api/search?keyword={} ] {} Get Reagent Property Data from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            reagent = get_Table_data(self.__keyword)
            if reagent:
                self.__pubchemData['ReagentProperty']['Status'] = status.HTTP_200_OK
                self.__pubchemData['ReagentProperty']['Contents'] = reagent
            else:
                self.__pubchemData['ReagentProperty']['Status'] = status.HTTP_404_NOT_FOUND

    def __sendSynonymDataToDBMS(self, casNo, data):
        pass

    def __sendReagentDataToDBMS(self, data):
        try:
            requests.post('http://0.0.0.0:8089/create/reagent', data=data, timeout=0.1)
        except requests.exceptions.ReadTimeout:
            pass
        
