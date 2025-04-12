from django.contrib import admin
from .models import Misecllaneous

class MisecllaneousAdmin(admin.ModelAdmin):
    list_display = ['misecllaneousTitle', 'misecllaneousVideo', 'misecllaneousCreateAt']

admin.site.register(Misecllaneous, MisecllaneousAdmin)