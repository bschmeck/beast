from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import mail
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template

from datetime import date, datetime, time, timedelta
import json
import random
import string
import sys

from forms import AccountInfoForm, RegistrationForm, WorkoutForm
from models import City, Location, Message, UserProfile, Workout

def workoutNotify(workout, action, changeMsg=None):
    if action == "Modified" or action == "Deleted":
        toAddrs = workout.confirmed.values_list('email', flat=True) | workout.interested.values_list('email', flat=True)
        msg = get_template('workouts/workout_notify_update.email').render(Context({
            'workout': workout,
            'changeMsg': changeMsg,
            'action': action.lower(),
            'url': 'http://beast.shmk.org',
            'command_url': 'http://beast.shmk.org/faq#commands',
            }))
    elif action == "Joined" or action == "Dropped":
        toAddrs = list(workout.confirmed.filter(userprofile__notify_adddrop=True).values_list('email', flat=True))
        toAddrs.extend(list(workout.interested.filter(userprofile__notify_adddrop=True).values_list('email', flat=True)))
        if workout.notify_organizer and workout.organizer.email not in toAddrs:
            toAddrs.append(workout.organizer.email)

        msg = get_template('workouts/workout_notify_adddrop.email').render(Context({
            'workout': workout,
            'changeMsg': changeMsg
            }))
    elif action == "Created":
        toAddrs = UserProfile.objects.filter(notify=True).values_list('user__email', flat=True)
        msg = get_template('workouts/workout_notify_create.email').render(Context({
            'workout': workout,
            'url': 'http://beast.shmk.org',
            'command_url': 'http://beast.shmk.org/faq#commands',
            }))
    else:
        raise ValueError("Unknown action %s" % action)

    # Don't bother sending mail if we don't have any addresses
    if not toAddrs:
        return

    subj = "BEAST Workout %s -- %s -- %s" % (action, workout.title, workout.startDate.strftime("%A %Y-%m-%d"))
    fromAddr = workout.addr()

    messages = []
    messages.append(mail.EmailMessage(subj, msg, fromAddr, toAddrs))
    conn = mail.get_connection()
    conn.send_messages(messages)

def genChangeText(field, old, new):
    return '%s changed from:\n%s\nto:\n%s\n' % (field, old, new)

def dateStr(d):
    if d:
        return date.strftime(d, "%m/%d/%Y")

    return "None"
def timeStr(t):
    if t:
        return time.strftime(t, "%I:%M %p")

    return "None"

@login_required
def account(request):
    today = datetime.now().date()
    u = request.user.get_profile()

    if request.method == 'POST':
        f = AccountInfoForm(request.POST, instance=u)
        ret = {}
        ret["success"] = False
        if f.is_valid():
            f.save()
            ret["success"] = True
        else:
            msg = ''
            for k, v in f.errors:
                msg += "%(k): %(v)\n"
            ret["msg"] = msg
        return HttpResponse(json.dumps(ret), "application/javascript")
    else:
        w = request.user.confirmed_workouts.filter(startDate__gte=today)    
        f = AccountInfoForm(instance=u)
        return render_to_response('workouts/account.djhtml',
                                  {'form': f,
                                   'workouts': w},
                                  context_instance=RequestContext(request))

@login_required
def deleteWorkout(request, w_id):
    w = get_object_or_404(Workout, pk=w_id)
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    ret = {}
    ret["success"] = False
    if request.user != w.organizer:
        ret["errMsg"] = "You do not have permission to delete this workout."
    else:
        try:
            msg = Message()
            msg.msgType = 'CHANGE'
            msg.workout = w
            msg.sender = request.user
            msg.msgDate = datetime.now() + timedelta(hours=1)
            msg.text = "This workout has been deleted."
            workoutNotify(w, "Deleted", msg)
            w.delete()
            ret["success"] = True            
        except:
            ret["errMsg"] = "Error during deletion."
    return HttpResponse(json.dumps(ret), "application/javascript")

@login_required
def updateWorkout(request, w_id):
    w = get_object_or_404(Workout, pk=w_id)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=w)
        # Copy out the fields we want to track updates to, as soon as we call
        # is_valid() the workout object will be updated.
        old_title = w.title
        old_date = w.startDate
        old_time = w.startTime
        old_loc = w.location
        old_wTime = w.warmupTime
        old_desc = w.description

        if form.is_valid():
            changeText = ''
            if old_title != w.title:
                changeText += genChangeText('Title', old_title, w.title)
            if old_date != w.startDate:
                changeText += genChangeText('Date', dateStr(old_date), dateStr(w.startDate))
            if old_time != w.startTime:
                changeText += genChangeText('Go Time', timeStr(old_time), timeStr(w.startTime))
            if old_loc != w.location:
                changeText += genChangeText('Location', old_loc, w.location)
            if old_wTime != w.warmupTime:
                changeText += genChangeText('Warmup Time', timeStr(old_wTime), timeStr(w.warmupTime))
            if old_desc != w.description:
                changeText += genChangeText('Description', old_desc, w.description)
 
            with transaction.commit_on_success():
                form.save()
                if changeText != '':
                    msg = Message()
                    msg.msgType = 'CHANGE'
                    msg.workout = w
                    msg.sender = request.user
                    msg.msgDate = datetime.now() + timedelta(hours=1)
                    msg.text = changeText
                    msg.save()

                    workoutNotify(w, "Modified", msg)

            return HttpResponseRedirect('/')
            
    else:
        form = WorkoutForm(instance=w)
    locations = Location.objects.order_by('name')
    locationStr = str(','.join(map(lambda n: '"' + n + '"', locations.values_list('name', flat=True))))
    return render_to_response('workouts/edit.djhtml',
                              {'form': form,
                               'action': 'update',
                               'w_id': w_id,
                               'locationStr': locationStr,
                               'locations': locations},
                              context_instance=RequestContext(request))
@login_required
def createWorkout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            # We need to set organizer manually.  If we don't set commit=False
            # the save will fail since organizer isn't set.
            workout = form.save(commit=False)
            workout.organizer = request.user
            workout.save()
            request.user.confirmed_workouts.add(workout)

            workoutNotify(workout, "Created")
            return HttpResponseRedirect("/")
    else:
        form = WorkoutForm(initial={'city': request.user.get_profile().primary_city.pk})

    locations = Location.objects.order_by('name')
    locationStr = str(','.join(map(lambda n: '"' + n + '"', locations.values_list('name', flat=True))))
    return render_to_response('workouts/edit.djhtml',
                              {'form': form,
                               'action': 'create',
                               'locationStr': locationStr,
                               'locations': locations,
                               'firstDay': request.user.get_profile().js_weekStart()},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_anonymous)
def accountCreate(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            displayName = form.cleaned_data['displayName']
            notify = form.cleaned_data['notify']
            weekStart = form.cleaned_data['weekStart']
            city = form.cleaned_data['primary_city']
            
            with transaction.commit_on_success():
                username = genUserName()
                new_user = User.objects.create_user(username=username,
                                                    email = email,
                                                    password=pwd)
                new_user.save()

                profile = UserProfile()
                profile.user = new_user
                profile.displayName = displayName
                profile.notify = notify
                profile.weekStart = weekStart
                profile.primary_city = city
                profile.save()

            user = auth.authenticate(username=username, password=pwd)
            if user and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render_to_response('registration/register.djhtml',
                              {'form': form},
                              context_instance=RequestContext(request))

def genUserName():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        ret = ''.join(random.choice(chars) for x in range(20))
        try:
            User.objects.get(username=ret)
        except User.DoesNotExist:
            return ret

class CalendarDay:
    def __init__(self, dte, in_past):
        self.dte = dte
        self.workouts = []
        self.in_past = in_past

    def addWorkout(self, w, highlight):
        self.workouts.append((w, highlight))

    def dateStr(self):
        return datetime.strftime(self.dte, "%m/%d")

def calendar(request, slug=None):
    city = None
    if slug:
        city = get_object_or_404(City, slug=slug)
    if request.user.is_authenticated():
        weekStart = request.user.get_profile().weekStart
        if not city:
            city = request.user.get_profile().primary_city
    else:
        weekStart = 6
        if not city:
            city = City.objects.first()
    alt_cities = City.objects.exclude(id=city.id)
    
    d = datetime.now().date()
    # weekday() gives Monday as 0, Sunday as 6
    # Back up the correct number of days to reach the start day
    adj = ((d.weekday() - weekStart) + 7) % 7
    d -= timedelta(days=adj)

    days = []
    daysDone = False
    ret = []
    t = timedelta(days=1)
    for i in range(4):
        w = []
        while True:
            if not daysDone:
                days.append(d.strftime('%A'))
            in_past = d < datetime.now().date()
            c = CalendarDay(d, in_past=in_past)
            for workout in city.workouts.filter(startDate=d).order_by("startTime"):
                if request.user.is_authenticated():
                    highlight = request.user in workout.confirmed.all() or request.user in workout.interested.all()
                else:
                    highlight = False
                c.addWorkout(workout, highlight)
            w.append(c)
            d += t
            if d.weekday() == weekStart:
                daysDone = True
                break
        ret.append(w)
    return render_to_response('workouts/calendar.djhtml',
                              {'days': days,
                               'weeks': ret,
                               'city': city,
                               'alt_cities': alt_cities},
                              context_instance=RequestContext(request))

def getWorkout(request, w_id):
    w = get_object_or_404(Workout, pk=w_id)
    confirmed = map(lambda u: u.get_profile().displayName, w.confirmed.all())
    interested = map(lambda u: u.get_profile().displayName, w.interested.all())
    messages = w.message_set.all().order_by("-msgDate")
    try:
        loc = Location.objects.get(name=w.location)
        locText = loc.description
    except Location.DoesNotExist:
        locText = None

    if request.user.is_authenticated:
        showJoin = not request.user in w.confirmed.all()
        showMaybe = not request.user in w.interested.all()
        showDrop = not (showJoin and showMaybe)
        canUpdate = request.user == w.organizer
    else:
        showJoin = False
        showMaybe = False
        showDrop = False
        canUpdate = False

    return render_to_response('workouts/workout.djhtml',
                              {'workout': w,
                               'confirmed': confirmed,
                               'interested': interested,
                               'showJoin': showJoin,
                               'showMaybe': showMaybe,
                               'showDrop': showDrop,
                               'canUpdate': canUpdate,
                               'messages': messages,
                               'locText': locText},
                              context_instance=RequestContext(request))

@login_required
def joinWorkout(request, w_id):
    w = get_object_or_404(Workout, pk=w_id)
    try:
        action = request.POST["action"]
    except KeyError:
        return HttpResponseBadRequest("Missing argument")

    changeStr = None
    if action == "join":
        action = "Joined"
        request.user.confirmed_workouts.add(w)
        request.user.possible_workouts.remove(w)
        changeStr = "%s joined the workout" % request.user.get_profile().displayName
    elif action == "maybe":
        action = "Joined"
        request.user.confirmed_workouts.remove(w)
        request.user.possible_workouts.add(w)
        changeStr = "%s is a maybe for the workout" % request.user.get_profile().displayName
    else:
        action = "Dropped"
        request.user.confirmed_workouts.remove(w)
        request.user.possible_workouts.remove(w)
        changeStr = "%s dropped the workout" % request.user.get_profile().displayName

    if changeStr:
        m = Message(msgType="CHANGE", workout=w, text=changeStr, sender=request.user, msgDate=datetime.now()+timedelta(hours=1))
        m.save()
        workoutNotify(w, action, m)
        
    confirmed = map(lambda u: u.get_profile().displayName, w.confirmed.all())
    interested = map(lambda u: u.get_profile().displayName, w.interested.all())
    showJoin = not request.user in w.confirmed.all()
    showMaybe = not request.user in w.interested.all()
    showDrop = not (showJoin and showMaybe)
    cellText = get_template('workouts/calendar_cell_text.djhtml').render(Context({'workout': w}))
    ret = {"confirmed": ",".join(confirmed),
           "interested": ",".join(interested),
           "showJoin": showJoin,
           "showMaybe": showMaybe,
           "showDrop": showDrop,
           "cellText": cellText}
    return HttpResponse(json.dumps(ret), "application/javascript")

def faq(request):
    return render_to_response('workouts/faq.djhtml',
                              {},
                              context_instance=RequestContext(request))
