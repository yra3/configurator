from django.urls import path
from homepage import views
from configure.views import find_configure
urlpatterns = [
    path('c', find_configure),
    path('', views.index),
    path('auto/', views.auto),

]


