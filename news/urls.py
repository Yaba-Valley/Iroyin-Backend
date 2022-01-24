from django.urls import path
from . import views

urlpatterns = [
    path('get_news/', views.index, name = 'index route'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    # path('test_templates/', views.test_templates, name = 'test_template'),
    # path('profile/', views.profile, name = 'profile')
]