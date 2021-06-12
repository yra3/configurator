from django.urls import path
from homepage import views
from configure.views import simple_configure, extended_configure
urlpatterns = [
    path('simple/find/', simple_configure),
    path('extended/find/', extended_configure),
    path('simple/', views.auto),
    path('extended/', views.preauto),
]


