from django.db import models
from django.contrib.auth.models import User

class BooksRead(models.Model):
    'Contains books which are already read'
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    num_pages = models.IntegerField('number of pages')
    read_date = models.DateTimeField('date finished reading')
    comment = models.CharField(max_length=300) # idea about book after reading
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: add a "read | not read" status
    
    def __str__(self):
        return self.name

class Books2Read(models.Model):
    'Contains books which are already read'
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: add a Field to show who proposed the book
    
    def __str__(self):
        return self.name


