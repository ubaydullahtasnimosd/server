from django.contrib import admin
from .models import Visitor

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')

admin.site.register(Visitor, VisitorAdmin)