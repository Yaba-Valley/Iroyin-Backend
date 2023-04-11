from django.contrib import admin

from .models import Interest, News, Website

# Register your models here.

admin.site.register(Interest)

class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title']
    show_full_result_count = True


admin.site.register(News, NewsAdmin)
admin.site.register(Website)

