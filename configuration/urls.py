from django.urls import path
from django.views.generic import TemplateView
from configuration.views import component, configuration_view

urlpatterns = [
    path('<cpu>/<gpu>/<mother>/<ram>/<cooler>/<ssd>/<hdd>/<ps>/', configuration_view),
    path('<component_name>/<component_id>/', component),
]


