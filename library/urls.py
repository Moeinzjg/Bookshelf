from django.urls import path
from . import views


urlpatterns = [
    path('submit/booksread/', views.submit_BooksRead, name='submit_BooksRead'),
    path('submit/books2read/', views.submit_Books2Read, name='submit_Books2Read'),
    path('accounts/register/', views.register, name='register'),
]