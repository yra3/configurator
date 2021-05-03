from django.urls import path
from homepage import views
from configure.views import find_configure, find_configure2
urlpatterns = [
    path('c', find_configure),
    path('b', find_configure2),
    path('', views.index),
    path('auto/', views.auto),

]


