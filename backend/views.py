from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import requests
import json
import math
import subprocess

from .models import Landmark

# Create your views here.


def optimal(home, landmarks, time_left, obj, index_array):
    no_of_landmarks = len(landmarks)
    current = home
    next = []
    path = [home]
    step = 0
    landmark_array = []


    while step < no_of_landmarks:

        current = path[-1]
        minimum = float("inf")

        for i in xrange(0,no_of_landmarks):
            position = [landmarks[i].latitude,landmarks[i].longitude]

            if not position in path:
                dist = distance(current,position,obj,index_array)

                if dist < minimum:
                    minimum = dist
                    next = position

        path.append(next)
        ind = index_array.index(next)

        if ind < no_of_landmarks:
            landmark_array.append(landmarks[ind])

        step += 1

    return path, landmark_array


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
            ind = index_array.index(next)
            landmark_array.append(landmarks[ind])

    # for p in path:
    #     ind = index_array.index(p)

    #     if ind >= no_of_landmarks:
    #         continue
    #     else:
    #         landmark_array.append(landmarks[ind])

    return path, landmark_array


def find_next_landmark(home, current, landmarks, path, time_left, obj, index_array):
    minimum = float("inf")
    next = []

    for i in xrange(0,len(landmarks)):
        position = [landmarks[i].latitude,landmarks[i].longitude]

        if not position in path:
            time_foward = distance(current,position,obj,index_array)
            time_back = distance(position,home,obj,index_array)
            visit_time = landmarks[i].duration*60.0

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

    avg_speed = 35.0 # speed in mph

    radius = 20.0

    time = time * 60.0 * 60.0 # into seconds

    print radius
    print time

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)
    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    key = "AIzaSyBkn91vJ3YoVNJm_eTaPbKMKDuEEDdZiQ4"

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

    r = requests.get(url)

    obj = r.json()

    path, landmark_array = tour_plan([latitude,longitude], landmarks, time, obj, index_array)

    opti_path, opti_landmarks = optimal([latitude,longitude], landmark_array, time, obj, index_array)

    print opti_path

    if len(path) > 1:
        content = serializers.serialize("json", opti_landmarks)
    else:
        content = opti_landmarks

    return HttpResponse(content, content_type="application/json")

def update(request):

    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])

    radius = 20.0 #in miles

    lat_range = get_latitude_range(radius)
    long_range = get_longitude_range(latitude,radius)

    landmarks = Landmark.objects.filter(latitude__range=(latitude-lat_range, latitude+lat_range)).filter(longitude__range=(longitude-long_range, longitude+long_range))

    content = serializers.serialize("json", landmarks)

    return HttpResponse(content, content_type="application/json")


