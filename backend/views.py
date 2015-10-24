from django.shortcuts import render
import requests
import json

# Create your views here.

def send(request):

    return render(request, "send.html", {})


def receive(request):

    data = request.GET['text']

    print data

    content = {
        "data": data,
    }

    return render(request, "receive.html", content)

def tour(request):

    key = "AIzaSyBS_jDhoFpwRRS68Nfct_9RxQVGCpsaam4"

    time = 60 * 60 * 2
    landmarks = [43.082706,-79.074184,42.584810,-78.043524,42.876345,-78.878969,42.905689,-78.843432]
    position = [42.954632,-78.817884]

    params = ""
    param_array = []

    for l in xrange(0,len(landmarks),2):
        param_array.append(str(landmarks[1])+","+str(landmarks[l+1]))

    params = "|".join(param_array)

    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+params+"&destinations="+params+"key="+key)

    obj = json.load(r.text)

    calc_path()

    #obj.rows.elements[i].duration[j].value

    pass

def calc_path():

    #TODO

    pass

