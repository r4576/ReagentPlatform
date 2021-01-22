from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import MolecularData
from api.serializers import MolecularSerializer


class SignIn(APIView):
    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

class SignOut(APIView):
    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

class Search(APIView):
    def get(self, request, format=None):
        queryset = MolecularData.objects.all()
        serializer = MolecularSerializer(queryset, many=True)
        return Response({"molecular" : serializer.data}, status=status.HTTP_200_OK)
