from django import forms
from django.utils.translation import ugettext_lazy as _

from art979.Event.models import Event

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
