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
    return render(request, 'humantest/login.html', {})

NUM_QAS = len(QA.objects.all())
NUM_FINISHED = 0

SETTINGS = [i for i in os.listdir('../metadata/')]
print(SETTINGS)


def start(request, setting='long_uniform', phase='test'):
    # find not answered question
    user = get_user(request)
    unanswered_qa = QA.objects.exclude(answerers__icontains=user.username)
    global NUM_FINISHED
    NUM_FINISHED = NUM_QAS - len(unanswered_qa)
    print(NUM_FINISHED)
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

    return render(request, "humantest/qa.html", context)

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

# Create your views here.
