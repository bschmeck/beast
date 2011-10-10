from django.db import models
from django.forms import ModelForm

from workouts.models import Workout

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class': 'datePicker'})
    return formfield

class WorkoutForm(ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'title',
            'startDate',
            'startTime',
            'location',
            'warmupTime',
            'description']
    class Meta:
        model = Workout
        exclude = ('organizer', 'confirmed', 'interested', 'tags')
