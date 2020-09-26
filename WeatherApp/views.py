from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = '9b185a328e000dbbd9255ab086904cc9'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid + '& lang =ru'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Город не найден!'
            else:
                err_msg = 'Город уже есть в базе!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город успешно добавлен!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

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
    context = {'all_info': all_cities, 'form': form, 'message': message, 'message_class': message_class}
    return render(request, 'weatherapp/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('Weatherapp:home')
