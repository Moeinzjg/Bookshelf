import random
import string
from datetime import datetime
import requests
from postmark import PMMail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from library.models import User, Token, BooksRead, Books2Read
from library.models import Passwordresetcodes

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# TODO: Add Google Captcha
def grecaptcha_verify(request):
    data = request.POST
    captcha_rs = data.get('g-recaptcha-response')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,   #! need to get Google Captcha  
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)


def register(request):
    if 'requestcode' in request.POST.keys(): #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        #is this spam? check reCaptcha
        # ! Add captcha
        if not grecaptcha_verify(request): # captcha was not correct
            context = {'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'} #TODO: forgot password
            return render(request, 'register.html', context)

        if User.objects.filter(email = request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username = request.POST['username']).exists(): #if user does not exists
                code = random_str(48)
                now = datetime.now()
                email = request.POST['email']
                password = make_password(request.POST['password'])
                username = request.POST['username']
                temporarycode = Passwordresetcodes (email = email, time = now, code = code, username=username, password=password)
                temporarycode.save()
                # !: make the url site in the text body of below message
                message = PMMail(api_key = settings.POSTMARK_API_TOKEN,
                                 subject = "فعال سازی اکانت قفسه",
                                 sender = "moeinzjg@gmail.com",
                                 to = email,
                                 text_body = "برای فعال سازی ایمیلی قفسه خود روی لینک روبرو کلیک کنید: {}?email={}&code={}".format(request.build_absolute_url('/accounts/register/'), email, code),
                                 tag = "account request")
                message.send()
                context = {'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
                return render(request, 'index.html', context)
        else:
            context = {'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET.keys(): # user clicked on code
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = random_str(48)
            Token.objects.create(user=newuser, token=this_token)
            Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
            context = {'message': 'اکانت شما ساخته شد. توکن شما {} است. آنرا ذخیره کنید، چون دیگر نمایش داده نخواهد شد! جدی'.format(this_token)}
            return render(request, 'index.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


def index(request):
    context = {'message': ''}
    return render(request, 'index.html', context)



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