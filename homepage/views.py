from django.shortcuts import render
from .forms import Configuration


def index(request):
    return render(request, "configure/index.html")


def auto(request):
    return render(request, "configure/auto.html")


def preauto(request):
    from configure.models import CPU
    socket = CPU.objects.all().distinct('socket')
    context = {
        'socket': socket,
        '123':12
    }

    return render(request, "configure/preauto.html", context=context)

# def config(request):
#     return render(request, "configure/config.html")


