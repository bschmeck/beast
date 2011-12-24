from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template import Context
from django.template.loader import get_template

from datetime import date, datetime
import email

from beast.workouts.models import Workout

def dateStr(d):
    if d:
        return date.strftime(d, "%m/%d/%Y")
    return "Unknown"

class Command(BaseCommand):
    args = ''
    help = 'Emails notifications for today\'s workouts'

    def notifyMsg(self, w):
        subj = "Workout Today"
        fromAddr = w.addr()
        toAddrs = w.confirmed.values_list('email', flat=True) | w.interested.values_list('email', flat=True)
        conf_list = ",".join(w.confirmed.values_list('userprofile__displayName', flat=True))
        if conf_list == '':
            conf_list = 'None'
        maybe_list = ",".join(w.interested.values_list('userprofile__displayName', flat=True))
        if maybe_list == '':
            maybe_list = 'None'
        body = get_template('workouts/workout_notify_today.email').render(Context({'workout': w,
                                                                                   'conf_list': conf_list,
                                                                                   'maybe_list': maybe_list}))
        return mail.EmailMessage(subj, body, fromAddr, toAddrs)
    
    def handle(self, *args, **options):
        ws = Workout.objects.filter(startDate__exact=datetime.today().date())
        messages = []
        for w in ws:
            messages.append(self.notifyMsg(w))
        conn = mail.get_connection()
        conn.send_messages(messages)
                                 
