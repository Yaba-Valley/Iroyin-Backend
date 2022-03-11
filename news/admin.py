from django.contrib import admin

from .models import Interest, User, News

# Register your models here.

admin.site.register(User)
admin.site.register(News)
admin.site.register(Interest)