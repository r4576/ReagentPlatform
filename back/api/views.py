from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import MolecularData
from api.serializers import MolecularSerializer
from datetime import datetime


class Search(APIView):
    def get(self, request, format=None):
        keywords = request.GET.get('keyword')
        response = {
            "OK" : [],
            "NotFound" : [],
            "Result" : []
        }
        
        for keyword in keywords.split(','):
            queryset = MolecularData.objects.filter(formula=keyword)
            serializer = MolecularSerializer(queryset, many=True)
            if serializer.data:
                response['OK'].append(keyword)
                response['Result'].append(serializer.data[0])
                print("[ /api/search/keyword=" + keyword + " ]", datetime.now(), "HTTP_200_OK")
            else:
                response['NotFound'].append(keyword)
                print("[ /api/search/keyword=" + keyword + " ]", datetime.now(), "HTTP_404_NotFound")
            
        return Response(response, status=status.HTTP_200_OK)

