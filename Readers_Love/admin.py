from django.contrib import admin
from .models import Readers_Love

class ReadersLoveAdmin(admin.ModelAdmin):
    list_display = ['readersBookImg', 'readersBookName', 'readersName', 'readersReview', 'readersReviewCreated']

admin.site.register(Readers_Love, ReadersLoveAdmin)