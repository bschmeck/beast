from django.contrib.auth.models import User
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from beast.workouts.models import Message, Workout

from datetime import datetime
import email
import re
import sys

class Command(BaseCommand):
    args = ''
    help = 'Processes an incoming mail message.'

    def beastOp(self, workout, user, opStr):
        action = opStr.split("[BEAST] ")[1].lower()
        changeStr = None
        if action == "join":
            request.user.confirmed_workouts.add(workout)
            request.user.possible_workouts.remove(workout)
            changeStr = "%s joined the workout" % user.email
        elif action == "maybe":
            request.user.confirmed_workouts.remove(workout)
            request.user.possible_workouts.add(workout)
            changeStr = "%s is a maybe for the workout" % user.email
        elif action == "drop":
            request.user.confirmed_workouts.remove(workout)
            request.user.possible_workouts.remove(workout)
            changeStr = "%s dropped the workout" % user.email

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
            user = User.objects.get(email=msg['From'])
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
        if user and body:
            for line in body.splitlines():
                if line.startswith("[BEAST] "):
                    self.beastOp(workout, user, line)
        if body:
            msgText = body
        else:
            msgText = html

        # Save the message
        m = Message(msgType="MAIL", workout=workout, text=msgText, sender=user, msgDate=datetime.now())
        m.save()

        # Finally, forward it on to everyone signed up for the workout
        subj = "Message About Workout %s on %s" % (workout.title, str(workout.startDate))
        fromAddr = msg['To']
        toAddrs = []
        for u in workout.confirmed.all():
            toAddrs.append(u.email)
        for u in workout.interested.all():
            toAddrs.append(u.email)

        conn = mail.get_connection()
        messages = []
        messages.append(mail.EmailMessage(subj, msgText, fromAddr, toAddrs))
        conn.send_messages(messages)
