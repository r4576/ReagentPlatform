import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_DIR = os.path.join(os.path.join(ROOT_DIR, 'service'), 'dataset')
sys.path.append(SERVICE_DIR)

from reagent_property_data_Pubchem import get_query, get_Table_data
from api.models import Synonym, MaterialSafetyData, ReagentPropertyData
from api.serializers import SynonymSerializer, MaterialSafetyDataSerializer, ReagentPropertyDataSerializer
from datetime import datetime


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
            'ReagentProperty' : { },
            'Synonym' : []
        }
        
    def initializeData(self):
        self.__data['Keyword'] = None
        self.__data['Name'] = None
        self.__data['ReagentProperty'] = None
        self.__data['MaterialSafety'] = None
        self.__keyword = None
        self.__casNo = None
        self.__pubchemData['ReagentProperty'] = { }
        self.__pubchemData['Synonym'] = [ ]

    @property
    def data(self):
        if self.__casNo:
            return self.__data
        else:
            print("[ InternalServerError ] {} call findData function first".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return None

    @data.setter
    def data(self, keyword):
        self.__keyword = keyword
        self.__data['Keyword'] = keyword
        self.__data['Name'] = self.__getName()
        self.__data['ReagentProperty'] = self.__getReagentProperty()
        self.__data['MaterialSafety'] = self.__getMaterialSafety()

    def findData(self, keyword):
        self.initializeData()
        self.data = keyword

    def __getName(self):
        queryset = Synonym.objects.filter(subName=self.__keyword)
        serializer = SynonymSerializer(queryset, many=True)
        print("[ /api/search?keyword={} ] {} {} result(s) found in Keyword Collections".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(serializer.data)))
        if serializer.data:
            self.__casNo = serializer.data[0]['casNo']
            return serializer.data[0]['mainName']
        else:
            self.__getDataFromPubchem()
            for name in self.__pubchemData['Synonym']:
                if not Synonym.objects.filter(subName=name):
                    Synonym.objects.create(mainName=self.__pubchemData['ReagentProperty']['name'], subName=name, casNo=self.__pubchemData['ReagentProperty']['casNo'])
            self.__casNo = self.__pubchemData['ReagentProperty']['casNo']
            return self.__getName()
            
    def __getReagentProperty(self):
        queryset = ReagentPropertyData.objects.filter(casNo=self.__casNo)
        serializer = ReagentPropertyDataSerializer(queryset, many=True)
        if serializer.data:
            print("[ /api/search?keyword={} ] {} {} Reagent property Data HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), serializer.data[0]['id']))
            return serializer.data[0]
        else:
            self.__getDataFromPubchem()
            print(self.__pubchemData['ReagentProperty'])
            ReagentPropertyData.objects.create( casNo=self.__pubchemData['ReagentProperty']['casNo'], \
                                                formula=self.__pubchemData['ReagentProperty']['formula'], \
                                                molecularWeight=self.__pubchemData['ReagentProperty']['molecularWeight'], \
                                                meltingpoint=self.__pubchemData['ReagentProperty']['meltingpoint'], \
                                                boilingpoint=self.__pubchemData['ReagentProperty']['boilingpoint'], \
                                                density=self.__pubchemData['ReagentProperty']['density'] )
            return self.__getReagentProperty()

    def __getMaterialSafety(self):
        queryset = MaterialSafetyData.objects.filter(casNo=self.__casNo)
        serializer = MaterialSafetyDataSerializer(queryset, many=True)
        if serializer.data:
            print("[ /api/search?keyword={} ] {} {} Material Safety Data HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), serializer.data[0]['id']))
            return serializer. data[0]
        else:
            print("[ /api/search?keyword={} ] {} No Material Safety Data HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return None

    def __getDataFromPubchem(self):
        if not self.__pubchemData['Synonym']:
            print("[ /api/search?keyword={} ] {} get Synonyms from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__pubchemData['Synonym'] = get_query(self.__keyword)
            if not self.__keyword in self.__pubchemData['Synonym']:
                self.__pubchemData['Synonym'].append(self.__keyword)
        if not self.__pubchemData['ReagentProperty']:
            print("[ /api/search?keyword={} ] {} get Reagent Property from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__pubchemData['ReagentProperty'] = get_Table_data(self.__keyword)

