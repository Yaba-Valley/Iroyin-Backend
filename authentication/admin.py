from django.contrib import admin
from .models import User, SearchQuery


admin.site.register(User)
admin.site.register(SearchQuery)