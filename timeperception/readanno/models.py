from django.db import models

# Create your models here.

class Task(models.Model):
	taskid = models.IntegerField()
	descp = models.CharField(max_length=10000)

class Document( models.Model):
    taskid = models.IntegerField()
    task = models.ForeignKey(Task)
    docid = models.IntegerField()
    relevance = models.IntegerField()
    content = models.CharField(max_length=30000)

class Setting(models.Model):
    settingid = models.IntegerField()

class SettingUnit(models.Model):
	settingid = models.IntegerField()
	sequence = models.IntegerField()
	taskid = models.IntegerField()
	docid = models.IntegerField()

class Log(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    action = models.CharField(max_length=20)
    query = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)

class Outcome(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    answer = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)

class TimeEstimation(models.Model):
    studentID = models.CharField(max_length=50)
    task_id = models.IntegerField()
    time = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)