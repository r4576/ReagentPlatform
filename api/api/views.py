from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.collector import Collector


class Search(APIView):
    def get(self, request, format=None):
        keywords = request.GET.get('keyword')
        response = []

        collector = Collector()
        for keyword in keywords.split(','):
            collector.execute(keyword)
            response.append(collector.data.copy())

        return Response(response, status=status.HTTP_200_OK)


