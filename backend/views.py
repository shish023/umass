from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import math
import subprocess

from .models import Landmark

# Create your views here.


def tour_plan(home, landmarks, time_left, obj, index_array):
    path = [home]
    no_of_landmarks = len(landmarks)
    current = home
    landmark_array =  []

    while(len(path) < no_of_landmarks):

        current = path[-1]
        next = find_next_landmark(home, current, landmarks, path, time_left, obj, index_array)

        if not next:
            return path, landmark_array
        else:
            time_left -= distance(current,next,obj,index_array)
            path.append(next)

    for p in path:
        ind = index_array.index(p)

        if ind >= no_of_landmarks:
            continue
        else:
            landmark_array.append(landmarks[ind])

    return path, landmark_array


def find_next_landmark(home, current, landmarks, path, time_left, obj, index_array):
    minimum = float("inf")
    next = []

    for i in xrange(0,len(landmarks)):
        position = [landmarks[i].latitude,landmarks[i].longitude]

        if not position in path:
            time_foward = distance(current,position,obj,index_array)
            time_back = distance(position,home,obj,index_array)
            visit_time = landmarks[i].duration

            time = time_foward+visit_time+time_back

            if time > time_left:
                pass
            else:

                if time < minimum:
                    minimum = time
                    next = position

    return next

def distance(src, dest, obj, index_array):
    src_index = index_array.index(src)
    dest_index = index_array.index(dest)
    print src_index
    print dest_index
    time = obj["rows"][src_index]["elements"][dest_index]["duration"]["value"]
    return int(time)


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

    time = time  * 60 * 60 # into seconds

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)
    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    key = "AIzaSyBzznQtkrL18nK1bDyrSQkCbYOyFJTinp4"

    parameters = ""
    param_array = []
    index_array = []

    for l in landmarks:
        param_array.append(str(l.latitude)+","+str(l.longitude))
        index_array.append([l.latitude,l.longitude])

    param_array.append(str(latitude)+","+str(longitude))
    index_array.append([latitude,longitude])


    parameters = "|".join(param_array)

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+parameters+"&destinations="+parameters+"&key="+key

    print url

    r = requests.get(url)

    obj = r.json()

    path, landmark_array = tour_plan([latitude,longitude], landmarks, time, obj, index_array)

    if len(landmark_array) > 1:
        content = serializers.serialize("json", landmark_array)
    else:
        content = landmark_array



    return HttpResponse(content, content_type="application/json")

def update(request):

    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])

    radius = 100.0 #in miles

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)

    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    content = serializers.serialize("json", landmarks)

    return HttpResponse(content, content_type="application/json")


