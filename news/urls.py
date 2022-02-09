from django.urls import path
from . import views

urlpatterns = [
    path('get_news/', views.index, name='index route'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('indicate_news_interaction/', views.indicate_interaction,
         name='indicate news interaction')
]
