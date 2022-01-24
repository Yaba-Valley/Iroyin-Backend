from django.urls import path
from . import views

urlpatterns = [
    path('get_news/', views.index, name = 'index route'),
    # path('user_seen_news/', views.user_seen_news, name = 'user_seen_news'),
    path('test_templates/', views.test_templates, name = 'test_template'),
    path('profile/', views.profile, name = 'profile')
]