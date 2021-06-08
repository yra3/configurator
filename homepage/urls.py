from django.urls import path, include
from homepage import views
# from configure.views import real_auto_configure, half_auto_configure, autopage, sborka
urlpatterns = [
    # path('a', real_auto_configure),
    # path('b', half_auto_configure),
    path('', views.index),
    path('auto/', views.auto),

    # path('auto/conf/', autopage),
    # path('config/', include('configure.urls')),
    # path('config/<cpu>/<gpu>/<mother>/<ram>/<cooler>/<ssd>/<hdd>/<ps>/', sborka)
]


