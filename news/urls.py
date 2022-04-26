from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    
    # AUTH URLS
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/activate-account/<str:uid>/<str:token>', views.activate_account, name = 'activate account'),
    
    # USER URLS
    # path('user/interests/', views.user_interest, name = 'user interests'),
    path('user/interests/add', views.save_interests, name = 'save user interests'),
    path('user/interests/remove', views.remove_interests, name = 'remove user interests'),
    
    #NEWS URLS
    path('news/get_news/', views.index, name='index route'),
    path('news/indicate_interaction/', views.indicate_interaction, name='indicate news interaction'),
    
    #STATICS
    path('interests/all', views.get_all_interests, name = 'get all interests'),
    
    path('test-jwt/', views.HelloView.as_view(), name = 'hello'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name = 'get jwt token')
    
]
