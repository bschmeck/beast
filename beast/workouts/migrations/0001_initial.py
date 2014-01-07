# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workout'
        db.create_table(u'workouts_workout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
            ('startTime', self.gf('django.db.models.fields.TimeField')()),
            ('warmupTime', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organzied_workouts', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('notify_organizer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'workouts', ['Workout'])

        # Adding M2M table for field confirmed on 'Workout'
        m2m_table_name = db.shorten_name(u'workouts_workout_confirmed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workout', models.ForeignKey(orm[u'workouts.workout'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workout_id', 'user_id'])

        # Adding M2M table for field interested on 'Workout'
        m2m_table_name = db.shorten_name(u'workouts_workout_interested')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workout', models.ForeignKey(orm[u'workouts.workout'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workout_id', 'user_id'])

        # Adding M2M table for field tags on 'Workout'
        m2m_table_name = db.shorten_name(u'workouts_workout_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workout', models.ForeignKey(orm[u'workouts.workout'], null=False)),
            ('tag', models.ForeignKey(orm[u'workouts.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workout_id', 'tag_id'])

        # Adding model 'Tag'
        db.create_table(u'workouts_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'workouts', ['Tag'])

        # Adding model 'UserProfile'
        db.create_table(u'workouts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify_adddrop', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('displayName', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('weekStart', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'workouts', ['UserProfile'])

        # Adding model 'Message'
        db.create_table(u'workouts_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msgType', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.Workout'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('msgDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'workouts', ['Message'])

        # Adding model 'Location'
        db.create_table(u'workouts_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'workouts', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Workout'
        db.delete_table(u'workouts_workout')

        # Removing M2M table for field confirmed on 'Workout'
        db.delete_table(db.shorten_name(u'workouts_workout_confirmed'))

        # Removing M2M table for field interested on 'Workout'
        db.delete_table(db.shorten_name(u'workouts_workout_interested'))

        # Removing M2M table for field tags on 'Workout'
        db.delete_table(db.shorten_name(u'workouts_workout_tags'))

        # Deleting model 'Tag'
        db.delete_table(u'workouts_tag')

        # Deleting model 'UserProfile'
        db.delete_table(u'workouts_userprofile')

        # Deleting model 'Message'
        db.delete_table(u'workouts_message')

        # Deleting model 'Location'
        db.delete_table(u'workouts_location')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'workouts.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'workouts.message': {
            'Meta': {'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msgDate': ('django.db.models.fields.DateTimeField', [], {}),
            'msgType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.Workout']"})
        },
        u'workouts.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'workouts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'displayName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_adddrop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'weekStart': ('django.db.models.fields.IntegerField', [], {})
        },
        u'workouts.workout': {
            'Meta': {'object_name': 'Workout'},
            'confirmed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'confirmed_workouts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'possible_workouts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notify_organizer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organzied_workouts'", 'to': u"orm['auth.User']"}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.TimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['workouts.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'warmupTime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['workouts']