from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import math
import subprocess

from .models import Landmark

# Create your views here.






def tour(home, landmarks, time_left, obj):
    path = [home]
    no_of_landmarks = len(landmarks)
    current = [home]

    while(len(path) < no_of_landmarks):

        next = find_next_landmark(home, current, landmarks, time_left)

        if next == []:
            return path
        else:
            path.append(next)
            time_left -= distance(current,next)
            current = next

    return path


def find_next_landmark(home, current, landmarks, time_left, obj):

    minimum = float("-inf")
    next = []

    for i in xrange(0,len(landmarks)):
        position = [landmarks[i].latitude,landmarks[i].longitude]
        if not position in path:
            time_foward = distance(current,position,obj)
            time_back = distance(position,home,obj)
            visit_time = landmarks[i].duration

            time = time_foward+visit_time+time_back

            if time > time_left:
                continue
            else:

                if time < minimum:
                    minimum = total
                    next = position

    return next

# def distance(src, dest, obj):
#     time = obj["rows"][index_src].elements[index_dest].duration.value
#     return time







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

    obj = r.json()



    #path = tour([latitude,longitude], landmarks, time, obj)



    return HttpResponse(obj["rows"][0]["elements"][0]["duration"]["text"], content_type="application/json")

def update(request):

    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])

    radius = 100.0 #in miles

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)

    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    content = serializers.serialize("json", landmarks)

    return HttpResponse(content, content_type="application/json")


