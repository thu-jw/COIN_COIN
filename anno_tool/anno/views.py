from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Video
import glob
import os

def index(request):
    return render(request, 'anno/index.html', {})

def anno(request, video_id, start_step):
    if video_id == 0:
        return HttpResponse("Congratulations! We have finished!")

    video = Video.objects.get(id=video_id)
    if start_step == video.steps:
        return HttpResponse("Current Video Finished" + str(video_id))

    print(os.getcwd())
    first_img = glob.glob('/opt/data5/COIN_COIN/{}/{}/img*.jpg'.format(
        video.video_name,
        start_step
    ))[-1]

    first_img = '/'.join(first_img.split('/')[-3:])

    if start_step < video.steps - 1:
        second_img = glob.glob('/opt/data5/COIN_COIN/{}/{}/img*.jpg'.format(
            video.video_name,
            start_step + 1
        ))[0]
        second_img = '/'.join(second_img.split('/')[-3:])
    else:
        second_img = None

    context = {
        "first_img": first_img,
        "second_img": second_img,
        "video": video
    }
    return render(request, 'anno/anno.html', context)

    # get path
    return HttpResponse("Test" + str(video_id))

def start(request):
    unfinished_videos = Video.objects.filter(state=0)
    try:
        if request.POST["submit"] == "continue":
            annotating_videos = Video.objects.filter(state=1)
            if len(annotating_videos) > 0:
                video_id = annotating_videos[0].id
            else:
                video_id = unfinished_videos[0].id
        else:
            video_id = unfinished_videos[0].id
        video = Video.objects.get(id=video_id)
        start_step = video.checkpoint
        return HttpResponseRedirect('../{}/{}'.format(video_id, start_step))
    except IndexError:
        return HttpResponseRedirect('../0/0')

# Create your views here.
