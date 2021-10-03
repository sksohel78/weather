from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('get_location/',views.GetLocation.as_view(), name='get_location'),
    path('add_point/', views.AddPoint.as_view(), name='add_point'),
    path('', views.Home.as_view(), name='home')
]
