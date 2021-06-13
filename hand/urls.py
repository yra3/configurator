from django.urls import path
from django.views.generic import TemplateView
from hand import views
urlpatterns = [
    path('', TemplateView.as_view(template_name="about_us/about.html",
         extra_context={"header": "О сайте"})),
    path('configuration/', views.configuration),
]


