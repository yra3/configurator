from django.shortcuts import render
from .forms import Configuration

def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        freac = request.POST.get("age")

        data = {"name": name, "freac": freac}
        return render(request, "homepage/index.html", context=data)
    header = "Personal Data"  # обычная переменная
    langs = ["English", "German", "Spanish"]  # массив
    user = {"name": "Tom", "age": 23}  # словарь
    addr = ("Абрикосовая", 23, 45)  # кортеж
    userform = Configuration()  # форма для заполнения
    from homepage.models import CPU
    p = CPU.objects.all()

    for ps in p:
        header += ps.link+ps.name


    data = {"header": header, "langs": langs, "user": user, "address": addr, "userform": userform}
    return render(request, "homepage/index.html", context=data)


def auto(request):
    return render(request, "homepage/auto.html")


