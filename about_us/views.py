from django.http import HttpResponse


def about(request):

    return HttpResponse('<h1>Главная страница сайта</h1>')

def searchConfigurate(request):

    pass
