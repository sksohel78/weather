from django.contrib.gis.geos import Point
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from .models import *
from .forms import *
import requests
# Create your views here.

class Home(View):
    def get(self, request):
        points = Location.objects.all()
        print(points[0].point.x, points[0].point.y)

        return render(request, 'index.html', {'points':points})

class AddPoint(View):
    def post(self, request):
        form = LocationForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            lat = form.cleaned_data.get('lat')
            lng = form.cleaned_data.get('lng')
            resp = requests.get('https://api.weather.gov/points/{0},{1}'.format(lat, lng))
            data = resp.json()
            try:
                if data['status'] == 404:
                    return JsonResponse({'status':0, 'Message':data['detail']})
            except KeyError:
                location = Location.objects.create(
                    name=name,
                    point = Point(lat, lng),
                    office = data['properties']['gridId'],
                    grid_x = data['properties']['gridX'],
                    grid_y = data['properties']['gridY']
                )
                points = Location.objects.all()
                html = render_to_string('points_include.html', {'points':points})
                return JsonResponse({'status':1, 'data':html})
        else:
            return JsonResponse({'status':0, 'Message':'Invalid input'})


class GetLocation(View):
    def post(self, request):
        id = request.POST.get('id')
        location = Location.objects.get(id=id)
        resp = requests.get('https://api.weather.gov/gridpoints/{0}/{1},{2}/forecast'.format(location.office, location.grid_x, location.grid_y))
        resp_data = resp.json()
        try:
            if resp_data['status'] == 404:
                return JsonResponse({'status':0, 'Message':'Unable to fetch data for this location'})
        except KeyError:
            periods = resp_data['properties']['periods'][:2]
            popup = render_to_string('popup.html', {'periods':periods, 'name':location.name})
            data = {
                'id': location.id,
                'lat': location.point.x,
                'lng': location.point.y,
                'name': location.name,
                'popup':popup
            }
            return JsonResponse({'status':1, 'data':data})