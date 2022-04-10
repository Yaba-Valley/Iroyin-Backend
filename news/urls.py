from django.urls import path
from . import views

urlpatterns = [
    path('get_news/', views.index, name='index route'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    
    path('user/interests/', views.user_interest, name = 'user interests'),
    
    path('interests/all', views.get_all_interests, name = 'get all interests'),
    
    
    path('indicate_news_interaction/', views.indicate_interaction,
         name='indicate news interaction')
]
