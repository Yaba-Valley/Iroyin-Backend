from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # USER URLS
    path('user/interests/', views.UserInterests.as_view(), name = 'user interests'),
    path('user/interests/add/', views.Save_Interests.as_view(), name = 'save user interests'),
    path('user/interests/remove/', views.Remove_Interests.as_view(), name = 'remove user interests'),
    
    #NEWS URLS
    path('', views.GetNews.as_view(), name='index route'),
    path('news/get_news/', views.GetNews.as_view(), name='index route'),
    path('news/indicate_interaction/', views.Indicate_Interaction.as_view(), name='indicate news interaction'),
    path('news/search/<str:title>', views.Search_News.as_view(), name = 'search for news'),
    
    #STATICS
    path('interests/all/', views.get_all_interests, name = 'get all interests'),
]
