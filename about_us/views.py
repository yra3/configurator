from django.http import HttpResponse
from homepage.models import Processor

def about(request):

    return HttpResponse('<h1>Главная страница сайта</h1>')

def searchConfigurate(request):

    pass
