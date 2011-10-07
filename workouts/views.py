from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from datetime import datetime, timedelta

from models import Workout

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
    return render_to_response('workouts/workout.html',
                              {'workout': w,
                               'confirmed': w.confirmed.all(),
                               'interested': w.interested.all()},
                              context_instance=RequestContext(request))
