from django.urls import path
from . import views

app_name = 'Weatherapp'
urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),

]
