from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze_text/", views.analyze_text, name="analyze_text"),
    path("analyze_pdf/", views.analyze_pdf, name="analyze_pdf"),
    path("analyze_voice/", views.analyze_voice, name="analyze_voice"),

]