from django.contrib.auth.models import User
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template import Context
from django.template.loader import get_template

from beast.workouts.models import Message, Workout

from datetime import date, datetime
import email
import re
import sys

def dateStr(d):
    if d:
        return date.strftime(d, "%m/%d/%Y")

    return "Unknown"

class Command(BaseCommand):
    args = ''
    help = 'Processes an incoming mail message.'

    def beastOp(self, workout, user, opStr):
        action = opStr.split("[BEAST] ")[1].lower()
        changeStr = None
        if action == "join":
            user.confirmed_workouts.add(workout)
            user.possible_workouts.remove(workout)
            changeStr = "%s joined the workout" % user.get_profile().displayName
        elif action == "maybe":
            user.confirmed_workouts.remove(workout)
            user.possible_workouts.add(workout)
            changeStr = "%s is a maybe for the workout" % user.get_profile().displayName
        elif action == "drop":
            user.confirmed_workouts.remove(workout)
            user.possible_workouts.remove(workout)
            changeStr = "%s dropped the workout" % user.get_profile().displayName

        if changeStr:
            m = Message(msgType="CHANGE", workout=workout, text=changeStr, sender=user, msgDate=datetime.now())
            m.save()

            
    def handle(self, *args, **options):
        try:
            msg = email.message_from_file(sys.stdin)
        except:
            raise CommandError("Unable to read from stdin")
        mtch = re.match('^beast\+(\d+)@beast.shmk.org', msg['To'])
        if mtch:
            w_id = int(mtch.group(1))
        else:
            raise CommandError("Unable to parse 'To' field. [%s]" % msg['To'])
        try:
            workout = Workout.objects.get(pk=w_id)
        except Workout.DoesNotExist:
            raise CommandError("Unable to find workout with id %d" % w_id)
        try:
            fromAddr = email.utils.parseaddr(msg['From'])[1]
            user = User.objects.get(email=fromAddr)
        except User.DoesNotExist:
            user = None

        body = None
        html = None
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                if not body:
                    body = ""
                body += unicode(part.get_payload(decode=True), part.get_content_charset(), 'replace').encode('utf8', 'replace')
            elif part.get_content_type() == "text/html":
                if not html:
                    html = ""
                html += unicode(part.get_payload(decode=True), part.get_content_charset(), 'replace').encode('utf8', 'replace')
    
        if not body and not html:
            return
        
        # Process the body of the message, looking for beast commands
        # Only do this if the user exists
        # Don't forward BEAST commands to the mailing list
        foundOp = False
        if user and body:
            for line in body.splitlines():
                if line.startswith("[BEAST] "):
                    self.beastOp(workout, user, line)
                    foundOp = True
        if foundOp:
            return
        
        if body:
            msgText = body
        else:
            msgText = html

        # Save the message, if we know the sender
        if user:
            m = Message(msgType="MAIL", workout=workout, text=msgText, sender=user, msgDate=datetime.now())
            m.save()

        # Finally, forward it on to everyone signed up for the workout
        subj = "Message About Workout %s on %s" % (workout.title, str(workout.startDate))
        fromAddr = msg['To']
        toAddrs = workout.confirmed.values_list('email', flat=True) | workout.interested.values_list('email', flat=True)
        body = get_template('workouts/workout_notify_msg.email').render(Context({'dateStr': dateStr(m.msgDate),
                                                                                 'sender': user if user else fromAddr,
                                                                                 'msgText': msgText}))
        conn = mail.get_connection()
        messages = []
        messages.append(mail.EmailMessage(subj, body, fromAddr, toAddrs))
        conn.send_messages(messages)
