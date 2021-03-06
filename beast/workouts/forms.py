from django import forms
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from beast.workouts.models import City, UserProfile, Workout

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class': 'datePicker'})
    return formfield

class WorkoutForm(forms.ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'city',
            'title',
            'startDate',
            'startTime',
            'location',
            'warmupTime',
            'description',
            'notify_organizer']
    startTime = forms.TimeField(input_formats=("%I:%M %p",
                                         "%I:%M%p",
                                         "%I %p",
                                         "%I%p",
                                         "%H:%M"),
                                widget=forms.TimeInput(format='%I:%M %p'))
    warmupTime = forms.TimeField(input_formats=("%I:%M %p",
                                         "%I:%M%p",
                                         "%I %p",
                                         "%I%p",
                                         "%H:%M"),
                                 widget=forms.TimeInput(format='%I:%M %p'),
                                 required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label=None)
    
    def clean_startDate(self):
        data = self.cleaned_data['startDate']
        if data < datetime.today().date():
            raise forms.ValidationError("Invalid date.  You cannot create a workout in the past, McFly.")
        return data

    class Meta:
        model = Workout
        exclude = ('organizer', 'confirmed', 'interested', 'tags')

class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=30, label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Re-Enter Password')
    displayName = forms.CharField(max_length=30, label='Name To Display')
    weekStart = forms.ChoiceField(choices=((6, 'Sunday'),
                                           (0, "Monday"),
                                           (1, "Tuesday"),
                                           (2, "Wednesday"),
                                           (3, "Thursday"),
                                           (4, "Friday"),
                                           (5, "Saturday")), label='First Day Of The Week')
    primary_city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label=None)
                                           
    notify = forms.BooleanField(required=False, initial=True, label='Notify Me Of New Workouts')
    notify_adddrop = forms.BooleanField(required=False, initial=False, label='Notify Me As People Add/Drop Workouts I\'m Running')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already exists with that email address.")

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        pwd = cleaned_data.get("password")
        pwd1 = cleaned_data.get("password1")
        
        if pwd and pwd1:
            if pwd != pwd1:
                raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class AccountInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'displayName',
            'primary_city',
            'weekStart',
            'notify',
            'notify_adddrop',
            'cities'
            ]
        self.fields['cities'].queryset = City.objects.exclude(id=self.instance.primary_city_id)
    displayName = forms.CharField(max_length=30, label='Name To Display')
    weekStart = forms.ChoiceField(choices=((6, 'Sunday'),
                                           (0, "Monday"),
                                           (1, "Tuesday"),
                                           (2, "Wednesday"),
                                           (3, "Thursday"),
                                           (4, "Friday"),
                                           (5, "Saturday")), label='First Day Of The Week')
                                           
    notify = forms.BooleanField(required=False, initial=True, label='Notify Me Of New Workouts')
    notify_adddrop = forms.BooleanField(required=False, initial=False, label='Notify Me As People Add/Drop Workouts I\'m Running')
    primary_city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label=None)
    cities = forms.ModelMultipleChoiceField(queryset=City.objects.all(), label='Notify Me Of Workouts In These Other Cities', required=False)
