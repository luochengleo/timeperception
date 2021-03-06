from django.db import models


# Create your models here.

class Task(models.Model):
    taskid = models.IntegerField()
    descp = models.CharField(max_length=10000)

class Document(models.Model):
    taskid = models.IntegerField()
    docid = models.IntegerField()
    relevance = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=30000)

class SingleChoiceQuestionare(models.Model):
    taskid = models.IntegerField()
    docid = models.IntegerField()
    title = models.CharField(max_length=300)
    rightAnswer = models.CharField(max_length=30)
    choices = models.CharField(max_length=3000)

class Setting(models.Model):
    settingid = models.IntegerField()
    jobs = models.CharField(max_length=300)

class Job(models.Model):
    jobid  = models.IntegerField()
    settingid = models.IntegerField()
    taskid  = models.IntegerField()
    docseq = models.CharField(max_length=300)

class Log(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    action = models.CharField(max_length=20)
    query = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)

class Outcome(models.Model):
    studentid = models.CharField(max_length=50)
    task_id = models.IntegerField()
    answer = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)

class TimeEstimation(models.Model):
    studentid = models.CharField(max_length=50)
    taskid = models.IntegerField()
    time = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)


class Log(models.Model):
    studentid = models.CharField(max_length=50)
    jobid = models.IntegerField()
    action = models.CharField(max_length=20)
    content = models.CharField(max_length=5000)

