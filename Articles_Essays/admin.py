from django.contrib import admin
from .models import Articles_Essays

class articlesEssaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'articlesEssaysImg', 'articlesEssaysName', 'articlesEssaysAuthor', 'articlesEssaysDescription', 'articlesEssaysQRCodeScen', 'articlesEssaysQRCodeScenImg', 'articlesEssaysCreateAt', 'articlesEssaysUpdateAt']

admin.site.register(Articles_Essays, articlesEssaysAdmin)