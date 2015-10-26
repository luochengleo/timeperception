from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from models import *
from django import template
from Utils.Utils import *

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
    _d = Document.objects.get(taskid = Job.objects.get(settingid=settingid,jobid = jobid).taskid, docid = 1)

    article = ''
    for s in _d.content.split('\n'):
        if s.strip()!= '':
            article+='<p>'+s.strip()+'</p>\n'
    print 'article',article
    html = template.Template(open('templates/calibrate.html').read())
    c = template.Context({'article':article,'settingid':settingid,'jobid':jobid})

    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def read(request, settingid, jobid):
    job = Job.objects.get(settingid=settingid,jobid=jobid)
    taskid = job.taskid
    docs = str2numseq(job.docseq,'-')
    doc1 = docs[0]
    doc2 = docs[1]
    doc3 = docs[2]
    doc4 = docs[3]

    print taskid,doc1,doc2,doc3,doc4



    html= template.Template(open('templates/read.html').read())
    c = template.Context({'taskid':taskid,'doc1':doc1,'doc2':doc2,'doc3':doc3,'doc4':doc4})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def feedback(request, settingid, jobid):
    return HttpResponse(open('templates/feedback.html').read())

def docservice(request,taskid,docid):
    _d = Document.objects.get(taskid=taskid,docid = docid);
    content = ''
    for s in _d.content.split('\n'):
        if s.strip()!='':
            content +='<p>'+s.strip()+'</p>'
    return HttpResponse(content)