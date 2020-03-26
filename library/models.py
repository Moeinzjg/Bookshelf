from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    'contains one token for each user to conduct OAuth'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)
    # TODO: generate random 48-char-length tokens
    def __str__(self):
        return "{}-token".format(self.user)


class BooksRead(models.Model):
    'Contains books which are already read'
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    # num_pages = models.IntegerField('number of pages')
    # read_date = models.DateTimeField('date finished reading')
    # comment = models.CharField(max_length=300) # idea about book after reading
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: add a "read | not read" status
    def __str__(self):
        return '{}-{}'.format(self.title, self.user)

class Books2Read(models.Model):
    'Contains books which are already read'
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: add a Field to show who proposed the book
    def __str__(self):
        return '{}-{}'.format(self.title, self.user)


class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length = 120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #TODO: do not save password