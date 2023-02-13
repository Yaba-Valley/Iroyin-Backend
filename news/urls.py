from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # USER URLS
    path('user/interests/', views.UserInterests.as_view(), name='user interests'),
    path('user/interests/add/', views.Save_Interests.as_view(),
         name='save user interests'),
    path('user/interests/remove/', views.Remove_Interests.as_view(),
         name='remove user interests'),

    # NEWS URLS
    path('news/get_news/', views.Get_News.as_view(), name='get news'),
    path('news/indicate_interaction/', views.Indicate_Interaction.as_view(),
         name='indicate news interaction'),
    path('news/search/', views.Search_News.as_view(), name='search for news'),
    path('news/get-details/', views.Get_News_Details.as_view(),
         name='get news details'),
    path('news/redirect', views.Redirect_To_App.as_view(), name='redirect to app'),

    # STATICS
    path('interests/all', views.Get_All_Interests.as_view(),
         name='get all interests'),
]
