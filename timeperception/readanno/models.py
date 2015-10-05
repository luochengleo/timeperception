from django.db import models

# Create your models here.

class Document( models.Model):
    taskid = models.IntegerField()
    docid = models.IntegerField()
    relevance = models.IntegerField()
    content = models.CharField(max_length=30000)

class Setting(models.Model):
    settingid = models.IntegerField()




