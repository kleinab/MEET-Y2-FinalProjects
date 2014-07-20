from django.db import models
import datetime
from django.utils import timezone

class Student(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __unicode__(self):
        return self.username

class Subject(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(Student)
    def __unicode__(self):
        return self.name

class Assignment(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject)
    duedate = models.DateTimeField()
    def __unicode__(self):
        return self.name