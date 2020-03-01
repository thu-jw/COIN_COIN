from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user

import json
import glob
import os

from .models import QA
def index(request):
    return HttpResponseRedirect("/humantest/start")

NUM_QAS = len(QA.objects.all())
NUM_FINISHED = 0

SETTINGS = [i for i in os.listdir('../metadata/')]
print(SETTINGS)


@login_required(login_url='/accounts/login/')
def start(request, setting='', phase='test'):
    print(request.COOKIES)
    if setting == '':
        if 'qa_id' in request.COOKIES:
            qa_id = request.COOKIES['qa_id']
            setting = QA.objects.get(pk=qa_id).setting
        else:
            setting = 'long5'
    print(setting)
    # find not answered question
    user = get_user(request)
    selected = QA.objects.filter(setting=setting, phase=phase)
    unanswered_qa = selected.filter(answers='')
    if len(unanswered_qa) == 0:
        unanswered_qa = selected.exclude(answerers__contains=user.username)
    global NUM_FINISHED
    global NUM_QAS
    NUM_QAS = len(selected)
    NUM_FINISHED = NUM_QAS - len(unanswered_qa)
    if len(unanswered_qa) > 0:
        qa = unanswered_qa[0]
        return HttpResponseRedirect(f'/humantest/{qa.id}')
    else:
        return HttpResponse('finished!')

@login_required(login_url='/accounts/login/')
def qa(request, qa_id):
    qa = QA.objects.get(pk=qa_id)
    context = {
        'id': qa_id,
        'question': json.loads(qa.question),
        'choices': json.loads(qa.choices),
        'phase': qa.phase,
        'setting': qa.setting,
        'ratio_finished': NUM_FINISHED * 100 // NUM_QAS,
        'num_finished': NUM_FINISHED,
        'num_qas': NUM_QAS,
        'settings': SETTINGS,
    }
    for c in context['choices']:
        c['gifs'] = [f'{s}/action.gif' for s in c['steps']]

    response = render(request, "humantest/qa.html", context)
    response.set_cookie('qa_id', qa_id)
    return response

@login_required(login_url='/accounts/login/')
def choose(request, qa_id):
    qa = QA.objects.get(pk=qa_id)
    try:
        ans = request.POST["answer"]
        user = get_user(request)
        if qa.answers == '':
            qa.answers = ans
            qa.answerers = user.username
            qa.save()
        else:
            qa.answers += str(ans)
            qa.answerers += f',{user.username}'
            qa.save()
        return HttpResponseRedirect(f'../{qa.setting}/{qa.phase}/start')
    except KeyError:
        return HttpResponseRedirect(f'../{qa_id}')

@login_required(login_url='/accounts/login/')
def stat(request):
    user = get_user(request)
    qas = QA.objects.filter(answerers__contains=user.username)

    correct = {}
    num_answered = {}
    for qa in qas:
        key = f'{qa.setting}/{qa.phase}'
        index = qa.answerers.split(',').index(user.username)
        ans = int(qa.answers[index])
        if key in num_answered:
            num_answered[key] += 1
        else:
            num_answered[key] = 1
            correct[key] = 0
        if qa.correct_answer == ans:
            correct[key] += 1

    acc = {
        k: '{:.2f}%'.format(correct[k] * 100 / num_answered[k])
        if num_answered[k] > 0 else '/'
        for k in num_answered.keys()
    }

    context = {
        'correct': sorted(correct.items()),
        'num_answered': num_answered,
        'acc': acc,
    }
    return render(request, "humantest/stat.html", context)

# Create your views here.
