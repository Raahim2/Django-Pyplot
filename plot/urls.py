from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.upload_csv, name='upload_csv'), 
    path('plot/', views.generate_plot, name='generate_plot'), # N
    path('load_more_rows/', views.load_more_rows, name='load_more_rows'),

]