from logging import exception
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError, DefaultCredentialsError
from google.auth.transport.requests import Request

from accounts.models import Profile

from datetime import datetime
import requests
import json

# Google Social Login API
flow = Flow.from_client_secrets_file(client_secrets_file=settings.GOOGLE_API_SETTINGS_FILE, scopes=settings.GOOGLE_AUTH_SCOPES)
flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
googleAuthorizationURL, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)

# Kakaotalk Social Login API
kakaoAuthorizationURL = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=" + settings.KAKAO_REST_API_KEY + "&redirect_uri=" + settings.KAKAO_REDIRECT_URI
kakaoTokenURL = "https://kauth.kakao.com/oauth/token"
kakaoProfileRequestURL = "https://kapi.kakao.com/v2/user/me"

# Naver Social Login API
naverAuthorizationURL = "https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=" + settings.NAVER_CLIENT_ID + "&redirect_uri=" + settings.NAVER_REDIRECT_URI + "&state="
naverTokenURL = "https://nid.naver.com/oauth2.0/token"
naverProfileRequestURL = "https://openapi.naver.com/v1/nid/me"

class GoogleLogin(APIView):
    def get(self, request):
        return redirect(googleAuthorizationURL)


class GoogleCallback(APIView):
    def get(self, request, format=None):
        try:
            flow.fetch_token(authorization_response=request.build_absolute_uri().replace('http:', 'https:'))
            creds = flow.credentials
            userinfo = id_token.verify_oauth2_token(creds._id_token, Request(), creds._client_id)
            loginStatus = status.HTTP_200_OK
            
            user = Profile.objects.get(code=userinfo['sub'])
            print("[{}] GoogleLogin User:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), user.code))
        except GoogleAuthError as e:
            loginStatus = status.HTTP_401_UNAUTHORIZED
            print("[{}] GoogleLogin {}".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), e))
        except DefaultCredentialsError as e:
            loginStatus = status.HTTP_503_SERVICE_UNAVAILABLE
            print("[{}] GoogleLogin {}".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), e))
        except Profile.DoesNotExist:
            newUser = User.objects.create(email=userinfo['email'],
                                          username=datetime.now().strftime('%y%m%d%H%M%S'))
            newProfile = Profile.objects.create(user=newUser,
                                                code=userinfo['sub'],
                                                userName=userinfo['name'],
                                                history="")
            loginStatus = status.HTTP_200_OK
            print("[{}] GoogleLogin NewUser:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), newProfile.code))
        except:
            loginStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
            print("[{}] GoogleLogin {}".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), loginStatus))
        finally:
            return redirect(settings.BASE_URL['URL'], status=loginStatus)


class KakaoLogin(APIView):
    def get(self, request):
        return redirect(kakaoAuthorizationURL)


class KakaoCallback(APIView):
    def get(self, request, format=None):
        try:
            accessToken = self.__getAccessToken(request)
            userProfile = self.__getUserProfile(accessToken)
            loginStatus = status.HTTP_200_OK

            user = Profile.objects.get(code=userProfile['id'])
            print("[{}] KakaoLogin User:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), user.code))
        except Profile.DoesNotExist:
            newUser = User.objects.create(email=userProfile['kakao_account']['email'],
                                          username=datetime.now().strftime('%y%m%d%H%M%S'))
            newProfile = Profile.objects.create(user=newUser,
                                                code=userProfile['id'],
                                                userName=userProfile['kakao_account']['profile']['nickname'],
                                                history="")
            print("[{}] KakaoLogin NewUser:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), newProfile.code))
        except Exception as e:
            errMessage, loginStatus = e.args
            print(errMessage)
        finally:
            return redirect(settings.BASE_URL['URL'], status=loginStatus)

    def __getAccessToken(self, request):
        tokenParameter = { }
        tokenParameter['grant_type'] = 'authorization_code'
        tokenParameter['client_id'] = settings.KAKAO_REST_API_KEY
        tokenParameter['redirect_uri'] = settings.KAKAO_REDIRECT_URI
        tokenParameter['code'] = request.GET.get('code')
        tokenParameter['client_secret'] = settings.KAKAO_CLIENT_SECRET
        
        response = requests.post(kakaoTokenURL, data=tokenParameter)

        if response.status_code == 200:
            return json.loads(response.text)['access_token']
        elif response.status_code == 400:
            raise Exception("[{}] KakaoLogin GetAccessToken HTTP_400_BAD_REQUEST".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("[{}] KakaoLogin GetAccessToken HTTP_500_INTERNAL_SERVER_ERROR".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __getUserProfile(self, accessToken):
        profileParameter = { }
        profileParameter['Authorization'] = "Bearer " + accessToken

        response = requests.post(kakaoProfileRequestURL, headers=profileParameter)

        if response.status_code == 200:
            userProfile = json.loads(response.text)
            return userProfile
        elif response.status_code == 400:
            raise Exception("[{}] KakaoLogin GetUserProfile HTTP_400_BAD_REQUEST".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("[{}] KakaoLogin GetUserProfile HTTP_500_INTERNAL_SERVER_ERROR".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_500_INTERNAL_SERVER_ERROR)


class NaverLogin(APIView):
    def get(self, request):
        return redirect(naverAuthorizationURL + request.COOKIES['csrftoken'])
        

class NaverCallback(APIView):
    def get(self, request):
        try:
            accessToken = self.__getAccessToken(request)
            userProfile = self.__getUserProfile(accessToken)
            user = Profile.objects.get(code=userProfile['id'])
            loginStatus = status.HTTP_200_OK
            print("[{}] NaverLogin User:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), user.code))
        except Profile.DoesNotExist:
            newUser = User.objects.create(email=userProfile['email'],
                                          username=datetime.now().strftime('%y%m%d%H%M%S'))
            newProfile = Profile.objects.create(user=newUser,
                                                code=userProfile['id'],
                                                userName=userProfile['name'],
                                                history="")
            loginStatus = status.HTTP_200_OK
            print("[{}] NaverLogin NewUser:{} HTTP_200_OK".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S'), newProfile.code))
        except Exception as e:
            errMessage, loginStatus = e.args
            print(errMessage)
        finally:
            return redirect(settings.BASE_URL['URL'], status=loginStatus)

    def __getAccessToken(self, request):
        tokenParameter = { }
        tokenParameter['grant_type'] = 'authorization_code'
        tokenParameter['client_id'] = settings.NAVER_CLIENT_ID
        tokenParameter['client_secret'] = settings.NAVER_CLIENT_SECRET
        tokenParameter['code'] = request.GET.get('code')
        tokenParameter['state'] = request.GET.get('state')
        
        response = requests.post(naverTokenURL, data=tokenParameter)

        if response.status_code == 200:
            return json.loads(response.text)['access_token']
        elif response.status_code == 400:
            raise Exception("[{}] NaverLogin GetAccessToken HTTP_400_BAD_REQUEST".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("[{}] NaverLogin GetAccessToken HTTP_500_INTERNAL_SERVER_ERROR".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __getUserProfile(self, accessToken):
        profileParameter = { }
        profileParameter['Authorization'] = "Bearer " + accessToken

        response = requests.post(naverProfileRequestURL, headers=profileParameter)

        if response.status_code == 200:
            userProfile = json.loads(response.text)['response']
            return userProfile
        elif response.status_code == 401:
            raise Exception("[{}] NaverLogin GetUserProfile HTTP_401_UNAUTHORIZED".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_401_UNAUTHORIZED)
        elif response.status_code == 403:
            raise Exception("[{}] NaverLogin GetUserProfile HTTP_403_FORBIDDEN".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_403_FORBIDDEN)
        elif response.status_code == 404:
            raise Exception("[{}] NaverLogin GetUserProfile HTTP_404_NOT_FOUND".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_404_NOT_FOUND)
        else:
            raise Exception("[{}] NaverLogin GetUserProfile HTTP_500_INTERNAL_SERVER_ERROR".format(datetime.now().strftime('%d/%b/%Y %H:%M:%S')), status.HTTP_500_INTERNAL_SERVER_ERROR)

