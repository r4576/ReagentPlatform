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

            name, casID = getCasID(keyword)
            if casID:
                newData['Name'] = name
                newData['ReagentData'] = getReagentPropertyData(casID)
                newData['MaterialSafetyData'] = getMarterialSafetyData(casID)
                print("[ /api/search?keyword={} ] {} found in database 200_OK".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                newName, newReagentData, newMaterialSafetyData = getNewData(keyword)
                if newReagentData:
                    newData['Name'] = newName
                    newData['ReagentData'] = newReagentData
                    newData['MaterialSafetyData'] = newMaterialSafetyData
                else:
                    newData['Name'] = None
                    newData['ReagentData'] = None
                    newData['MaterialSafetyData'] = None
                    print("[ /api/search?keyword={} ] {} 404_NotFound".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            response.append(newData)

        return Response(response, status=status.HTTP_200_OK)


def getCasID(keyword):
    queryset = Keyword.objects.filter(keyword=keyword)
    serializer = KeywordSerializer(queryset, many=True)
    if serializer.data:
        return serializer.data[0]['mainKeyword'], serializer.data[0]['casNo']
    else:
        return None, None

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
    newReagentData = get_Table_data(keyword)
    if newReagentData:
        newCasID = newReagentData['casNo']
        newMainName = newReagentData['name']
        for name in get_query(newMainName):
            if not Keyword.objects.filter(keyword=name):
                Keyword.objects.create(mainKeyword=newMainName, keyword=name, casNo=newCasID)
                print("[ /api/search?keyword={} ] {} {} is added to Keyword collections".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name))
        if not ReagentPropertyData.objects.filter(casNo=newCasID):
            ReagentPropertyData.objects.create( casNo=newCasID, \
                                                formula=newReagentData['formula'], \
                                                molecularWeight=newReagentData['molecularWeight'], \
                                                meltingpoint=newReagentData['meltingpoint'], \
                                                boilingpoint=newReagentData['boilingpoint'], \
                                                density=newReagentData['density'] )
            print("[ /api/search?keyword={} ] {} {} is added to Reagent Property Collections".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), newMainName))
        reagentPropertyData = getReagentPropertyData(newCasID)
        materialSatetyData = getMarterialSafetyData(newCasID)
        return newMainName, reagentPropertyData, materialSatetyData
    return None, None, None
