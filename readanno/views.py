from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from models import *
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


def jobs(request, settingid):
    _setting  = Setting.object.get(settingid = settingid)
    _jobs = []
    for i in range(1,5,1):
        _jobs = Job.objects.get(settingid = settingid, )

    return HttpResponse(open('templates/jobs.html').read())


def calibrate(request, settingid, jobid):
    return HttpResponse(open('templates/calibrate.html').read())


def read(request, settingid, jobid):
    return HttpResponse(open('templates/read.html').read())


def feedback(request, settingid, jobid):
    return HttpResponse(open('templates/feedback.html').read())
