from django import forms
from art979.Story.models import Story, Update

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
