from django.urls import path
from django.views.generic import TemplateView
from configure.views import sborka, component
urlpatterns = [
    path('<cpu>/<gpu>/<mother>/<ram>/<cooler>/<ssd>/<hdd>/<ps>/', sborka),
    path('<component_name>/<component_id>/', component),
]


