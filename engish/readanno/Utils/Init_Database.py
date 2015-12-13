# -*- coding: utf-8 -*-
__author__ = 'franky'

import xml.dom.minidom
from readanno.models import Task, Document, SingleChoiceQuestionare
from readanno.models import Setting, Job


def import_tasks(filename):
    print "import tasks from", filename
    domtree = xml.dom.minidom.parse(filename)
    Tasks = domtree.documentElement
    tasks = Tasks.getElementsByTagName('task')
    for task in tasks:
        task_id = task.getElementsByTagName('task_id')[0].childNodes[0].data
        task_id = int(task_id)
        descp = task.getElementsByTagName('descp')[0].childNodes[0].data
        question = task.getElementsByTagName('question')[0].childNodes[0].data
        t = Task(taskid=task_id, descp=descp, question=question)
        t.save()
        documents = task.getElementsByTagName('Document')
        for document in documents:
            doc_id = document.getElementsByTagName('doc_id')[0].childNodes[0].data
            doc_id = int(doc_id)
            relevance = document.getElementsByTagName('relevance')[0].childNodes[0].data
            relevance = int(relevance)
            title = document.getElementsByTagName('title')[0].childNodes[0].data
            content = document.getElementsByTagName('content')[0].childNodes[0].data
            d = Document(taskid=task_id, docid=doc_id, relevance=relevance, title=title, content=content)
            d.save()


def import_settings(filename):
    print "import settings from", filename
    domtree = xml.dom.minidom.parse(filename)
    Settings = domtree.documentElement
    settings = Settings.getElementsByTagName('Setting')
    for setting in settings:
        settingid = setting.getElementsByTagName('settingid')[0].childNodes[0].data
        settingid = int(settingid)
        taskseq = setting.getElementsByTagName('taskseq')[0].childNodes[0].data
        s = Setting(settingid=settingid, jobs=taskseq)
        s.save()
        jobs = setting.getElementsByTagName('Job')
        jobid = 0
        for job in jobs:
            taskid = job.getElementsByTagName('taskid')[0].childNodes[0].data
            taskid = int(taskid)
            docseq = job.getElementsByTagName('docseq')[0].childNodes[0].data
            j = Job(jobid=jobid, settingid=settingid, taskid=taskid, docseq=docseq)
            j.save()
            jobid += 1


def init_default():
    import_tasks('data/English_tasks.xml')
    import_settings('data/English_settings.xml')
