from django.contrib.auth.models import User
from django.db import models

from datetime import date, time

class Workout(models.Model):
    startDate = models.DateField()
    startTime = models.TimeField()
    warmupTime = models.TimeField()
    location = models.CharField(max_length=128)
    description = models.TextField()
    organizer = models.ForeignKey(User, related_name='organzied_workouts')
    confirmed = models.ManyToManyField(User, related_name='confirmed_workouts')
    interested = models.ManyToManyField(User, related_name='possible_workouts')
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=50)

class Tag(models.Model):
    text = models.CharField(max_length=50)



    
