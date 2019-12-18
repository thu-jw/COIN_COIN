from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Video
import glob
import os
from .utils import load_action_dict

action_dict = load_action_dict()
last_video_id = None
action_names = None

def index(request):
    return render(request, 'anno/index.html', {})


def anno(request, video_id, start_step):
    if video_id == 0:
        return HttpResponse("Congratulations! We have finished!")

    video = Video.objects.get(id=video_id)

    start_step = min(video.steps - 1, start_step)
    video.checkpoint = start_step
    video.save()

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

    # prepare action names
    global last_video_id
    global action_names
    if last_video_id != video_id:
        action_ids = video.action_ids.split(',')
        action_names = [action_dict.get(int(i), '---missing name---') for i in action_ids]
        last_video_id = video_id

    context = {
        "first_img": first_img,
        "first_name": action_names[start_step],
        "second_name": action_names[start_step + 1] if second_img is not None else None,
        "second_img": second_img,
        "video": video,
        "action_names": action_names,
        "start_step": start_step,
    }
    return render(request, 'anno/anno.html', context)

def navigate(request, video_id):
    # next action or next video or next cut
    video = get_object_or_404(Video, pk=video_id)
    post = request.POST["submit"]
    if post == "cut":
        cuts = video.cut_points.split(',')
        if str(video.checkpoint) not in cuts:
            cuts.append(str(video.checkpoint))
        video.cut_points = ','.join(cuts)
        video.checkpoint += 1
        video.checkpoint = min(video.steps - 1, video.checkpoint)
        video.state = 1 # annotating
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))

    elif post == "new":
        video.state = 2 # finished
        video.save()
        unfinished_videos = Video.objects.filter(state=0)
        try:
            video = unfinished_videos[0]
            video_id = video.id
            start_step = video.checkpoint
        except:
            video_id = start_step = 0
        return HttpResponseRedirect('../{}/{}'.format(video_id, start_step))
    elif post == "next":
        # next action
        video.checkpoint += 1
        video.checkpoint = min(video.steps - 1, video.checkpoint)
        video.state = 1 # annotating
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))

    elif post == "previous":
        # next action
        video.checkpoint = max(0, video.checkpoint - 1)
        video.state = 1 # annotating
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))

def start(request):
    # start new annotation
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
