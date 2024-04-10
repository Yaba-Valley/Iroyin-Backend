from django.contrib import admin

from .models import Interest, News, Website

# Register your models here.

admin.site.register(Interest)

admin.site.register(News)
admin.site.register(Website)


