from django.contrib import admin
from django.urls import path
from plot import views

urlpatterns = [
    path('' , views.index , name="index"),
    path('pie' , views.pie , name="pie"),
    path('linear' , views.linear , name="linear"),
    path('bar' , views.bar , name="bar"),
    path('scatter' , views.scatter , name="scatter"),
    path('histogram' , views.histogram , name="histogram"),
    path('stem' , views.stem, name="stem"),
    path('stack' , views.stack, name="stack"),
    path('stair' , views.stair, name="stair"),
    path('hex' , views.hex, name="hex"),
    path('trip' , views.trip, name="trip"),


]