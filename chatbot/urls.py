from django.urls import path 
from . import views 

# urls for the chatbot
urlpatterns = [ 
    path('', views.chatbotAi, name ='chatbot'),
    path('login', views.login, name ='login'),
    path('register', views.newUser, name ='register'),
    path('logout', views.logout, name ='logout'),
]