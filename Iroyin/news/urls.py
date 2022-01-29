from django.urls import path
from . import views

urlpatterns = [
    path('get_news/', views.index, name = 'index route')    
]