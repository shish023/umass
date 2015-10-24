from django.shortcuts import render

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