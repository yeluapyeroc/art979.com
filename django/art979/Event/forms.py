from django import forms
from django.utils.translation import ugettext_lazy as _

from art979.Event.models import Event
from art979.Event.custom import RecurringDateInput, RecurringDateFormField

class CreateEventForm(forms.ModelForm):
    date = RecurringDateFormField(widget=RecurringDateInput)
    class Meta:
        model = Event

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
