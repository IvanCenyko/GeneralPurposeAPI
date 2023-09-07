from django.urls import path

from . import views

urlpatterns = [
    path("dolar-blue", views.dolar_blue, name="dolar_blue"),
    path("bgas", views.bgas, name="bgas")
]