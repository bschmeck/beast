# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('slug', models.CharField(unique=True, max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('city', models.ForeignKey(related_name='locations', to='workouts.City', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msgType', models.CharField(max_length=10, choices=[(b'MAIL', b'E-mail'), (b'CHANGE', b'Change')])),
                ('text', models.TextField()),
                ('msgDate', models.DateTimeField()),
                ('sender', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notify', models.BooleanField(default=True)),
                ('notify_adddrop', models.BooleanField(default=False)),
                ('displayName', models.CharField(max_length=50)),
                ('weekStart', models.IntegerField()),
                ('cities', models.ManyToManyField(related_name='alternate_users', to='workouts.City', blank=True)),
                ('primary_city', models.ForeignKey(related_name='primary_users', on_delete=django.db.models.deletion.SET_NULL, to='workouts.City', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startDate', models.DateField(verbose_name=b'Date')),
                ('startTime', models.TimeField()),
                ('warmupTime', models.TimeField(null=True, blank=True)),
                ('location', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=50)),
                ('notify_organizer', models.BooleanField(default=False, verbose_name=b'Notify Me On Add/Drop')),
                ('city', models.ForeignKey(related_name='workouts', on_delete=django.db.models.deletion.SET_NULL, to='workouts.City', null=True)),
                ('confirmed', models.ManyToManyField(related_name='confirmed_workouts', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('interested', models.ManyToManyField(related_name='possible_workouts', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('organizer', models.ForeignKey(related_name='organzied_workouts', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='workouts.Tag', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='workout',
            field=models.ForeignKey(to='workouts.Workout'),
        ),
    ]
