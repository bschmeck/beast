from django.contrib.auth.models import User
from django.db import models

from datetime import date, time

class Workout(models.Model):
    startDate = models.DateField()
    startTime = models.TimeField()
    warmupTime = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=128)
    description = models.TextField()
    organizer = models.ForeignKey(User, related_name='organzied_workouts')
    confirmed = models.ManyToManyField(User, related_name='confirmed_workouts', blank=True, null=True)
    interested = models.ManyToManyField(User, related_name='possible_workouts', blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.startDate) + " - " + self.title

class Tag(models.Model):
    text = models.CharField(max_length=50)
    
    def __unicode__(self):
        return text


    
