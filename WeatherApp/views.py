from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = '9b185a328e000dbbd9255ab086904cc9'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid + '& lang =ru'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    cities = City.objects.order_by('-id')[0:3]

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name.title(),
            'temp': res['main']['temp'],
            'hum': res['main']['humidity'],
            'wind': res['wind']['speed'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weatherapp/index.html', context)
