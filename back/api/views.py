from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Keyword, MaterialSafetyData, ReagentPropertyData
from api.serializers import KeywordSerializer, MaterialSafetyDataSerializer, ReagentPropertyDataSerializer
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
                print("[ /api/search?keyword={} ] {} 200_OK".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                newData['ReagentData'] = None
                newData['MaterialSafetyData'] = None
                print("[ /api/search?keyword={} ] {} 404_NotFound".format(keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            response.append(newData)

        return Response(response, status=status.HTTP_200_OK)


def getCasID(keyword):
    queryset = Keyword.objects.filter(keyword=keyword)
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
