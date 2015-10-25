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

    html = template.Template(open('templates/login.html').read())
    c = template.Context({'allsettings': settings})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def jobs(request, settingid):
    _setting = Setting.objects.get(settingid = settingid)
    jobsseq = [int(item) for item in _setting.jobs.split('-')]
    _jobs = []
    print jobsseq
    for i in jobsseq:
        try:
            print i
            _j =Job.objects.get(settingid = settingid,jobid = i)
            descp = Task.objects.get(taskid= _j.taskid).descp
            _jobs.append((settingid,i,descp))
        except:
            print 'Fail to find ',i


    html = template.Template(open('templates/jobs.html').read())
    c = template.Context({'jobs': _jobs})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def calibrate(request, settingid, jobid):
    return HttpResponse(open('templates/calibrate.html').read())


def read(request, settingid, jobid):
    return HttpResponse(open('templates/read.html').read())


def feedback(request, settingid, jobid):
    return HttpResponse(open('templates/feedback.html').read())
