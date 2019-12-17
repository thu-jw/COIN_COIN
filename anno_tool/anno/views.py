from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Video

def index(request):
    return render(request, 'anno/index.html', {})

def anno(request, video_id):
    return HttpResponse("Test" + str(video_id))

def start(request):
    if request.POST["submit"] == "continue":
        # continue the unfinished annotation
        return HttpResponseRedirect('../1')
    else:
        # start new annotation
        return HttpResponseRedirect('../2')

# Create your views here.
