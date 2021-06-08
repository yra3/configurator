from django.urls import path
from homepage import views
from configure.views import simple_configure, extended_configure, sborka
urlpatterns = [
    path('simple/find/', simple_configure),
    path('extended/find/', extended_configure),
    # path('', views.index),
    path('simple/', views.auto),
    path('extended/', views.preauto),
    # path('auto/conf/', autopage),
    # path('config/', simple_configure),
    # path('config/<cpu>/<gpu>/<mother>/<ram>/<cooler>/<ssd>/<hdd>/<ps>/', sborka)
]


