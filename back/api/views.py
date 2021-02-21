import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_DIR = os.path.join(os.path.join(ROOT_DIR, 'service'), 'dataset')
sys.path.append(SERVICE_DIR)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Keyword, MaterialSafetyData, ReagentPropertyData
from api.serializers import KeywordSerializer, MaterialSafetyDataSerializer, ReagentPropertyDataSerializer
from reagent_property_data_Pubchem import get_query, get_Table_data
from datetime import datetime

class Search(APIView):
    def get(self, request, format=None):
        keywords = request.GET.get('keyword')
        response = []
        
        for keyword in keywords.split(','):
            newData = {} 
            newData['Keyword'] = keyword

            newCasID = getCasID(keyword)
            if newCasID:
                newData['ReagentData'] = getReagentPropertyData(newCasID)
                newData['MaterialSafetyData'] = getMarterialSafetyData(newCasID)
                print("[ /api/search?keyword={} ] {} found in database 200_OK".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                newReagentData, newMaterialSafetyData = getNewData(keyword)
                if newReagentData:
                    newData['ReagentData'] = newReagentData
                    newData['MaterialSafetyData'] = newMaterialSafetyData
                    print("[ /api/search?keyword={} ] {} added to database 200_OK".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                else:
                    newData['ReagentData'] = None
                    newData['MaterialSafetyData'] = None
                    print("[ /api/search?keyword={} ] {} 404_NotFound".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            response.append(newData)

        return Response(response, status=status.HTTP_200_OK)


def getCasID(keyword):
    queryset = Keyword.objects.filter(mainKeyword=keyword)
    serializer = KeywordSerializer(queryset, many=True)
    if serializer.data:
        return serializer.data[0]['casNo']
    else:
        return None

def getReagentPropertyData(casNo):
    queryset = ReagentPropertyData.objects.filter(casNo=casNo)
    serializer = ReagentPropertyDataSerializer(queryset, many=True)
    if serializer.data:
        return serializer.data[0]
    else:
        return None

def getMarterialSafetyData(casNo):
    queryset = MaterialSafetyData.objects.filter(casNo=casNo)
    serializer = MaterialSafetyDataSerializer(queryset, many=True)
    if serializer.data:
        return serializer.data[0]
    else:
        return None

def getNewData(keyword):
    nameList = get_query(keyword)
    if nameList:
        mainName = nameList[0]
        newReagentData = get_Table_data(mainName)
        if newReagentData:
            newCasID = newReagentData['casNo']
            for name in nameList:
                Keyword.objects.create(mainKeyword=mainName, keyword=name, casNo=newCasID)
            ReagentPropertyData.objects.create( casNo=newReagentData['casNo'], 
                                                formula=newReagentData['formula'], 
                                                molecularWeight=newReagentData['molecularWeight'], 
                                                meltingpoint=newReagentData['meltingpoint'], 
                                                boilingpoint=newReagentData['boilingpoint'], 
                                                density=newReagentData['density'] )
            materialSatetyData = getMarterialSafetyData(newCasID)
            return newReagentData, materialSatetyData
        return None, None
    else:
        return None, None