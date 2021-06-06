from django.shortcuts import redirect
from django.conf import settings

from rest_framework import status
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request

from accounts.models import User

flow = Flow.from_client_secrets_file(client_secrets_file=settings.GOOGLE_API_SETTINGS_FILE, scopes=settings.GOOGLE_AUTH_SCOPES)
flow.redirect_uri = 'http://localhost:8000/accounts/google/callback'

authorization_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)


class GoogleLogin(APIView):
    def get(self, request):
        return redirect(authorization_url)


class GoogleCallback(APIView):
    def get(self, request, format=None):
        flow.fetch_token(authorization_response=request.build_absolute_uri().replace('http:', 'https:'))
        creds = flow.credentials
        userinfo = id_token.verify_oauth2_token(creds._id_token, Request(), creds._client_id)
        try:
            User.objects.get(email=userinfo['email'])
        except User.DoesNotExist:
            User.objects.create(email=userinfo['email'],
                                username=userinfo['email'],
                                first_name=userinfo['given_name'],
                                last_name=userinfo['family_name'])
        
        return redirect("http://localhost:80")

