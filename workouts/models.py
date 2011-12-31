from django.contrib.auth.models import User
from django.db import models

from datetime import date, time

class Workout(models.Model):
    startDate = models.DateField("Date")
    startTime = models.TimeField()
    warmupTime = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=128)
    description = models.TextField()
    organizer = models.ForeignKey(User, related_name='organzied_workouts')
    confirmed = models.ManyToManyField(User, related_name='confirmed_workouts', blank=True, null=True)
    interested = models.ManyToManyField(User, related_name='possible_workouts', blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    title = models.CharField(max_length=50)
    notify_organizer = models.BooleanField("Notify Me On Add/Drop", blank=True, default=False)
    
    def __unicode__(self):
        return str(self.startDate) + " - " + self.title

    def startDateStr(self):
        return date.strftime(self.startDate, "%m/%d/%Y")

    def addr(self):
        return "beast+%s@beast.shmk.org" % (str(self.pk))

class Tag(models.Model):
    text = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.text

class UserProfile(models.Model):
    notify = models.BooleanField(default=True)
    notify_adddrop = models.BooleanField(default=False, blank=True)
    displayName = models.CharField(max_length=50)
    weekStart = models.IntegerField()
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.displayName

class Message(models.Model):
    MESSAGE_CHOICES = (
        ("MAIL", "E-mail"),
        ("CHANGE", "Change"),
    )
    msgType = models.CharField(max_length=10, choices=MESSAGE_CHOICES)
    workout = models.ForeignKey(Workout)
    text = models.TextField()
    sender = models.ForeignKey(User, blank=True, null=True)
    msgDate = models.DateTimeField()

class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name
