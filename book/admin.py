from django.contrib import admin 
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'bookImage', 'bookTitle', 'bookPublication', 'bookDescription', 'bookPurchaseLink', 'bookCreatedAt', 'bookUpdateAt']

admin.site.register(Book, BookAdmin)