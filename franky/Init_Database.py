# -*- coding: utf-8 -*-
__author__ = 'franky'

import xml.dom.minidom
from readanno.models import Task, Document, SingleChoiceQuestionare


def import_tasks(filename):
    print "import tasks from", filename
    domtree = xml.dom.minidom.parse(filename)
    Tasks = domtree.documentElement
    tasks = Tasks.getElementsByTagName('task')
    for task in tasks:
        task_id = task.getElementsByTagName('task_id')[0].childNodes[0].data
        task_id = int(task_id)
        descp = task.getElementsByTagName('descp')[0].childNodes[0].data
        t = Task(taskid=task_id, descp=descp)
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
        single_choice = task.getElementsByTagName('Single_Choice_Questionare')[0]
        title = single_choice.getElementsByTagName('title')[0].childNodes[0].data
        rightAnswer = single_choice.getElementsByTagName('right_Answer')[0].childNodes[0].data
        rightAnswer = int(rightAnswer)
        choices = single_choice.getElementsByTagName('choices')[0].childNodes[0].data
        s = SingleChoiceQuestionare(taskid=task_id, title=title, rightAnswer=rightAnswer, choices=choices)
        s.save()


def init_default():
    import_tasks('franky/tasks.xml')
