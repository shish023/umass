from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import math
import subprocess

from .models import Landmark

# Create your views here.

def calc_path():

    #TODO

    pass

def get_latitude_range(miles):
    earth_radius = 3960.0
    return (miles/earth_radius)*180.0/math.pi

def get_longitude_range(latitude,miles):
    earth_radius = 3960.0
    r = earth_radius*math.cos(latitude*math.pi/180.0)
    return (miles/r)*180.0/math.pi

def send(request):

    # proc = subprocess.Popen("php /home/shishir/hackumass/umass/backend/script.php", shell=True, stdout=subprocess.PIPE)
    # script_response = proc.stdout.read()

    # print script_response

    return render(request, "send.html", {})


def receive(request):

    data = request.GET['text']

    print data

    content = {
        "data": data,
    }

    return render(request, "receive.html", content)

def tour(request):

    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])
    time = float(request.GET['time'])

    #radius = 10.0 # in miles

    avg_speed = 25.0 # speed in mph

    radius = avg_speed * time / 2.0

    print radius

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)

    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))



    key = "AIzaSyBS_jDhoFpwRRS68Nfct_9RxQVGCpsaam4"

    # time = 60 * 60 * 2
    # landmarks = [43.082706,-79.074184,42.584810,-78.043524,42.876345,-78.878969,42.905689,-78.843432]
    # position = [42.954632,-78.817884]

    parameters = ""
    param_array = []

    for l in landmarks:
        param_array.append(str(l.latitude)+","+str(l.longitude))

    parameters = "|".join(param_array)

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+parameters+"&destinations="+parameters+"&key="+key

    r = requests.get(url)

    return HttpResponse(r.text, content_type="application/json")

def update(request):

    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])

    radius = 1.0 #in miles

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)

    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    content = serializers.serialize("json", landmarks)

    return HttpResponse(content, content_type="application/json")


