from django import forms
from django.contrib.auth.models import User
from django.db import models


from workouts.models import Workout

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
            'title',
            'startDate',
            'startTime',
            'location',
            'warmupTime',
            'description']
    startTime = forms.TimeField(input_formats=("%I:%M %p",
                                         "%I:%M%p",
                                         "%I %p",
                                         "%I%p",
                                         "%H:%M"),
                                widget=forms.TimeInput(format='%I:%M %p'))
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
                                           
    notify = forms.BooleanField(required=False, initial=True, label='Notify Me Of New Workouts')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
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
