from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from art979.Profile.models import UserProfile, Band, Organization

class CreateBandForm(forms.ModelForm):
    class Meta:
        model = Band

class EditBandForm(forms.ModelForm):
    class Meta:
        model = Band

class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization

class EditOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(
            label = _('Username'),
            max_length = 45,
            regex = r'^\w+$',
            help_text = _('Required. 30 characters or fewer. Alphanumeric characters only (letters, digits, and underscores).'), 
            error_message = _('This field must contain only letters, numbers and underscores.')
            )
    password1 = forms.CharField(
            label = _('Password'),
            widget = forms.PasswordInput
            )
    password2 = forms.CharField(
            label = _('Password Confirmation'),
            widget = forms.PasswordInput
            )

    class Meta:
        model = UserProfile

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
