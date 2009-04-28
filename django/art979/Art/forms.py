from django import forms
from django.utils.translation import ugettext_lazy as _

from art979.Art.models import Song, Album, VisualPiece, LiteraturePiece, PerformingPiece, Food, Film

class CreateSongForm(forms.ModelForm):
    class Meta:
        model = Song

class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album

class CreateVisualPieceForm(forms.ModelForm):
    class Meta:
        model = VisualPiece

class CreateLiteraturePieceForm(forms.ModelForm):
    class Meta:
        model = LiteraturePiece

class CreatePerformingPieceForm(forms.ModelForm):
    class Meta:
        model = PerformingPiece

class CreateFoodForm(forms.ModelForm):
    class Meta:
        model = Food

class CreateFilmForm(forms.ModelForm):
    class Meta:
        model = Film
