from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from datetime import datetime, timedelta

from models import UserProfile, Workout

@user_passes_test(lambda u: u.is_anonymous)
def accountCreate(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        username = genUserName()
        if User.objects.filter(email = email).exists():
            return render_to_response('registration/register.html',
                                      {'err_msg': "An account already exists with that email address."},
                                      context_instance=RequestContext(request))

        new_user = User.objects.create_user(username=username,
                                            email = email,
                                            password=pwd)
        new_user.save()

        profile = UserProfile()
        profile.user = new_user
        try:
            dispName = request.POST['displayName']
        except KeyError:
            dispName = email
        profile.notify = True
        profile.save()

        user = auth.authenticate(username=username,
                                 password=pwd)
        if user and user.is_active:
            auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return render_to_response('registration/register.html',
                                  {},
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
    def __init__(self, dte):
        self.dte = dte
        self.workouts = []

    def addWorkout(self, w):
        self.workouts.append(w)

    def dateStr(self):
        return datetime.strftime(self.dte, "%m/%d")

def calendar(request):
    d = datetime.now().date()
    # weekday() gives Monday as 0, Sunday as 6
    # Subtracting weekday()+1 gives us a Sunday
    if d.weekday() != 6:
        d -= timedelta(days=d.weekday()+1)

    ret = []
    t = timedelta(days=1)
    for i in range(4):
        w = []
        while True:
            c = CalendarDay(d)
            for workout in Workout.objects.filter(startDate=d):
                c.addWorkout(workout)
            w.append(c)
            d += t
            if d.weekday() == 6:
                break
        ret.append(w)
    return render_to_response('workouts/calendar.html',
                              {'weeks': ret},
                              context_instance=RequestContext(request))

def workout(request, w_id):
    w = get_object_or_404(Workout, pk=w_id)
    confirmed = map(lambda u: u.get_profile().displayName, w.confirmed.all())
    interested = map(lambda u: u.get_profile().displayName, w.interested.all())
    return render_to_response('workouts/workout.html',
                              {'workout': w,
                               'confirmed': confirmed,
                               'interested': interested},
                              context_instance=RequestContext(request))
