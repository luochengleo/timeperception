from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from models import Setting
from django import template


def login(request):
    class tempt:
        def __init__(self, _idx, _t):
            idx = _idx
            temporal = _t

    settings = set()
    for t in Setting.objects.all():
        settings.add(t.settingid)
    allsettings = set()
    for s in settings:
        allsettings.add((s[0], s[1]))
        print s[0], s[1]
    html = template.Template(open('templates/login.html').read())
    c = template.Context({'allsettings': allsettings})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def tasks(request, settingId):
    return HttpResponse(open('templates/tasks.html').read())


def calibrate(request, taskid):
    return HttpResponse(open('templates/calibrate.html').read())


def read(request, taskid, docid):
    return HttpResponse(open('templates/read.html').read())


def feedback(request, taskid):
    return HttpResponse(open('templates/feedback.html').read())
