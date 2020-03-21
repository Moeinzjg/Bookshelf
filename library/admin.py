from django.contrib import admin

from .models import BooksRead, Books2Read, Token

admin.site.register(BooksRead)
admin.site.register(Books2Read)
admin.site.register(Token)