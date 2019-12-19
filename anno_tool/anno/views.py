from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Video
import glob
import os
from .utils import load_action_dict, parse_cuts

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

    cut_points, clips = parse_cuts(video)

    num_videos = len(Video.objects.all())
    num_finished = len(Video.objects.filter(state=2))
    ratio_finished = (num_finished * 100) // num_videos

    context = {
        "first_img": first_img,
        "first_name": action_names[start_step],
        "second_name": action_names[start_step + 1] if second_img is not None else None,
        "second_img": second_img,
        "video": video,
        "action_names": action_names,
        "start_step": start_step,
        "clip_info": str(clips),
        "cut_points": cut_points,
        "num_videos": num_videos,
        "num_finished": num_finished,
        "ratio_finished": ratio_finished,
    }
    return render(request, 'anno/anno.html', context)

def edit(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    post = request.POST["edit"]
    cuts = video.cut_points.split(',')
    cuts = [int(cut) for cut in cuts if cut != '']

    if post == "cut":
        if video.checkpoint not in cuts:
            cuts.append(video.checkpoint)
        cuts = sorted(cuts)
        video.cut_points = ','.join([str(cut) for cut in cuts])

        video.state = 1 # annotating
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))
    else:
        deleted_cut = int(post)
        if deleted_cut == -1: # delete all
            video.cut_points = ""
        else:
            cuts.remove(deleted_cut)
            video.cut_points = ",".join(map(str, cuts))
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))

def navigate(request, video_id):
    # navigate in actions and videos
    video = get_object_or_404(Video, pk=video_id)
    post = request.POST["submit"]

    if post == "pv": # previous video
        video = Video.objects.get(pk=video.prev_vid)
        return HttpResponseRedirect('../{}/{}'.format(video.id, video.checkpoint))

    elif post == "nv":# next video
        video.state = 2 # finished
        video.save()
        unfinished_videos = Video.objects.filter(state=0)
        try:
            video = unfinished_videos[0]
            video.prev_vid = video_id
            video.save()
            video_id = video.id
            start_step = video.checkpoint
        except:
            video_id = start_step = 0
        return HttpResponseRedirect('../{}/{}'.format(video_id, start_step))
    elif post == "na": # next action
        # next action
        video.checkpoint += 1
        video.checkpoint = min(video.steps - 1, video.checkpoint)
        video.state = 1 # annotating
        video.save()
        return HttpResponseRedirect('../{}/{}'.format(video_id, video.checkpoint))

    elif post == "pa": # previous action
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
