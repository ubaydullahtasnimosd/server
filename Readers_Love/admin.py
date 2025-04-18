from django.contrib import admin
from .models import Readers_Love_Img, Readers_Love

class ReadersLoveAdmin(admin.ModelAdmin):
    list_display = ['readersBookName', 'readersName', 'readersReview', 'readersReviewCreated']

class ReadersLoveImgAdmin(admin.ModelAdmin):
    list_display = ['readersBookImg', 'readersReviewCreated']

admin.site.register(Readers_Love, ReadersLoveAdmin)
admin.site.register(Readers_Love_Img, ReadersLoveImgAdmin)