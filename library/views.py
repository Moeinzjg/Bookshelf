from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from library.models import User, Token, BooksRead, Books2Read
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def submit_BooksRead(request):
    """ user submits a book which has been already read """

    # TODO: validate data, title, author, etc. might be invalid or fake
    # TODO: some of the arguments might be missed or blank
    this_title = request.POST['title']
    this_author = request.POST['author']
    this_publisher = request.POST['publisher']
    this_genre = request.POST['genre']
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    BooksRead.objects.create(title = this_title, author = this_author,
        publisher = this_publisher, genre = this_genre, user = this_user)

    return JsonResponse({
        'status': 'ok',
        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def submit_Books2Read(request):
    """ user submits a book proposed to be read """

    # TODO: validate data, title, author, etc. might be invalid or fake
    # TODO: some of the arguments might be missed or blank
    this_title = request.POST['title']
    this_author = request.POST['author']
    this_publisher = request.POST['publisher']
    this_genre = request.POST['genre']
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token = this_token).get()
    Books2Read.objects.create(title = this_title, author = this_author,
        publisher = this_publisher, genre = this_genre, user = this_user)

    return JsonResponse({
        'status': 'ok',
        }, encoder=DjangoJSONEncoder)