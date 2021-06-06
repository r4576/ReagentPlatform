from django.urls import path
from accounts import views

urlpatterns = [
    path('google/login', views.GoogleLogin.as_view()),
    path('google/callback', views.GoogleCallback.as_view()),
]
