from django.shortcuts import render
from .forms import Configuration

def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        freac = request.POST.get("age")

        data = {"name": name, "freac": freac}
        return render(request, "homepage/index.html", context=data)

    return render(request, "configure/index.html")


def auto(request):
    return render(request, "configure/auto.html")

def config(request):


    return render(request, "configure/config.html")


