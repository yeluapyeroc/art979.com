from django import forms
from art979.Venue.models import Venue

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
