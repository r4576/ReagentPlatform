import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_DIR = os.path.join(os.path.join(ROOT_DIR, 'service'), 'dataset')
sys.path.append(SERVICE_DIR)

from rest_framework import status
from reagent_property_data_Pubchem import get_query, get_Table_data
from api.models import Synonym, MaterialSafetyData, ReagentPropertyData
from api.serializers import SynonymSerializer, MaterialSafetyDataSerializer, ReagentPropertyDataSerializer
from datetime import datetime

from tasks import createSynonyms


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
        self.__data['Keyword'] = keyword
        self.__data['Name'] = self.__getName()
        self.__data['ReagentProperty'] = self.__getReagentProperty()
        self.__data['MaterialSafety'] = self.__getMaterialSafety()

    def execute(self, keyword):
        self.initializeData()
        self.data = keyword

    def __getName(self):
        queryset = Synonym.objects.filter(subName=self.__keyword)
        serializer = SynonymSerializer(queryset, many=True)
        if serializer.data:
            print("[ /api/search?keyword={} ] {} {} Synonym Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), serializer.data[0]['id']))
            self.__casNo = serializer.data[0]['casNo']
            return serializer.data[0]['mainName']
        else:
            print("[ /api/search?keyword={} ] {} No Synonym Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__getDataFromPubchem()
            if self.__pubchemData['Synonym']['Status'] == status.HTTP_200_OK:
                self.__casNo = self.__pubchemData['ReagentProperty']['Contents']['casNo']
                if not Synonym.objects.filter(subName=self.__keyword):
                    Synonym.objects.create(mainName=self.__pubchemData['ReagentProperty']['Contents']['name'], subName=self.__keyword, casNo=self.__casNo)
                createSynonyms.delay(self.__pubchemData['ReagentProperty']['Contents']['name'], self.__pubchemData['Synonym']['Contents'], self.__casNo)
                return self.__getName()
            elif self.__pubchemData['Synonym']['Status'] == status.HTTP_404_NOT_FOUND:
                print("[ /api/search?keyword={} ] {} No Synonym Data from Pubchem HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                return None
            else:
                print("[ /api/search?keyword={} ] {} HTTP_500_InternalServerError".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                return None
            
    def __getReagentProperty(self):
        queryset = ReagentPropertyData.objects.filter(casNo=self.__casNo)
        serializer = ReagentPropertyDataSerializer(queryset, many=True)
        if serializer.data:
            print("[ /api/search?keyword={} ] {} {} Reagent property Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), serializer.data[0]['id']))
            return serializer.data[0]
        else:
            print("[ /api/search?keyword={} ] {} No Reagent property Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.__getDataFromPubchem()
            if self.__pubchemData['ReagentProperty']['Status'] == status.HTTP_200_OK:
                ReagentPropertyData.objects.create( casNo=self.__pubchemData['ReagentProperty']['Contents']['casNo'], \
                                                    formula=self.__pubchemData['ReagentProperty']['Contents']['formula'], \
                                                    molecularWeight=self.__pubchemData['ReagentProperty']['Contents']['molecularWeight'], \
                                                    meltingpoint=self.__pubchemData['ReagentProperty']['Contents']['meltingpoint'], \
                                                    boilingpoint=self.__pubchemData['ReagentProperty']['Contents']['boilingpoint'], \
                                                    density=self.__pubchemData['ReagentProperty']['Contents']['density'] )
                return self.__getReagentProperty()
            elif self.__pubchemData['ReagentProperty']['Status'] == status.HTTP_404_NOT_FOUND:
                print("[ /api/search?keyword={} ] {} No Reagent Property Data from Pubchem HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                return None
            else:
                print("[ /api/search?keyword={} ] {} HTTP_500_InternalServerError".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                return None

    def __getMaterialSafety(self):
        queryset = MaterialSafetyData.objects.filter(casNo=self.__casNo)
        serializer = MaterialSafetyDataSerializer(queryset, many=True)
        if serializer.data:
            print("[ /api/search?keyword={} ] {} {} Material Safety Data from Database HTTP_200_OK".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), serializer.data[0]['id']))
            return serializer. data[0]
        else:
            print("[ /api/search?keyword={} ] {} No Material Safety Data from Database HTTP_404_NotFound".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return None

    def __getDataFromPubchem(self):
        if self.__pubchemData['Synonym']['Status'] is None:
            print("[ /api/search?keyword={} ] {} Get Synonym Data from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            synonym = get_query(self.__keyword)
            if synonym:
                self.__pubchemData['Synonym']['Status'] = status.HTTP_200_OK
            else:
                self.__pubchemData['Synonym']['Status'] = status.HTTP_404_NOT_FOUND
            self.__pubchemData['Synonym']['Contents'] = synonym

        if self.__pubchemData['ReagentProperty']['Status'] is None:
            print("[ /api/search?keyword={} ] {} Get Reagent Property Data from Pubchem".format(self.__keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            reagent = get_Table_data(self.__keyword)
            if reagent:
                self.__pubchemData['ReagentProperty']['Status'] = status.HTTP_200_OK
            else:
                self.__pubchemData['ReagentProperty']['Status'] = status.HTTP_404_NOT_FOUND
            self.__pubchemData['ReagentProperty']['Contents'] = get_Table_data(self.__keyword)

