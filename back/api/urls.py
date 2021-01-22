from django.urls import path
from api import views

urlpatterns = [
    path('in/', views.SignIn.as_view()),
    path('out/', views.SignOut.as_view()),
    path('search/', views.Search.as_view())
]
