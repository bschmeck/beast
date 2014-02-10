# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'City', fields ['name']
        db.create_unique(u'workouts_city', ['name'])


        # Changing field 'UserProfile.primary_city'
        db.alter_column(u'workouts_userprofile', 'primary_city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.City'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Workout.city'
        db.alter_column(u'workouts_workout', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['workouts.City']))

    def backwards(self, orm):
        # Removing unique constraint on 'City', fields ['name']
        db.delete_unique(u'workouts_city', ['name'])


        # Changing field 'UserProfile.primary_city'
        db.alter_column(u'workouts_userprofile', 'primary_city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workouts.City'], null=True))

        # Changing field 'Workout.city'
        db.alter_column(u'workouts_workout', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['workouts.City']))

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
        u'workouts.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
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
            'cities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['workouts.City']"}),
            'displayName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notify_adddrop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary_city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workouts.City']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'weekStart': ('django.db.models.fields.IntegerField', [], {})
        },
        u'workouts.workout': {
            'Meta': {'object_name': 'Workout'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workouts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['workouts.City']"}),
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