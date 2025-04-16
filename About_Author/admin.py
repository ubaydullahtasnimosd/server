from django.contrib import admin
from .models import AboutAuthor

class AboutAuthorAdmin(admin.ModelAdmin):
    list_display = ['aboutAuthorImg', 'aboutAuthorName', 'aboutAuthorDescription']

admin.site.register(AboutAuthor, AboutAuthorAdmin)