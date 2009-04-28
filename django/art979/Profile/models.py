from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

from art979.Category.models import ArtistCategory, MusicGenre
from art979.Venue.models import Venue

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    ## attributes
    url = models.URLField(_('url'), blank=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    bio = models.TextField(_('bio'), blank=True)
    location = models.CharField(_('location'), max_length=150, blank=True)
    birth_date = models.DateField(_('birth Date'), blank=True)
    occupation = models.CharField(_('occupation'), max_length=150, blank=True)
    interests = models.TextField(_('interests'), blank=True)
    zip = models.CharField(_('zip code'), max_length=10, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES)
    pub_date = models.DateTimeField(_('date created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    
    ## user_options
    confirmed = models.BooleanField(_('confirmed'), default=False, editable=False)
    artist_profile = models.BooleanField(_('artist profile option'), default=False)
    show_email = models.BooleanField(_('show email option'), default=False)
    has_avatar = models.BooleanField(_('has avatar option'), default=False)
    gets_updates = models.BooleanField(_('get updates option'), default=False)

    ## relations
    user = models.ForeignKey(User, unique=True, editable=False) ## AUTH_PROFILE_MODULE
    categories = models.ManyToManyField(ArtistCategory, blank=True, related_name="users")
    favorite_venues = models.ManyToManyField(Venue, blank=True, related_name="users")

    def _get_username(self):
        return self.user.username
    username = property(_get_username)

    def _get_email(self):
        return self.user.email
    email = property(_get_email)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        if artist_profile:
            return "/artists/%s/" % self.user.id
        return "/"

class Organization(models.Model):
    ## attributes
    name = models.CharField(_('name'), max_length=300)
    bio = models.TextField(_('bio'), )
    pub_date = models.DateTimeField(_('date created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    ## relations
    admin = models.ForeignKey(User, editable=False)
    members = models.ManyToManyField(User, blank=True, related_name="organizations", through="OrganizationMembership")

    def _get_stub_from_name(self):
        return self.name.tolower().replace(" ", "")
    stub = property(_get_stub_from_name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/organizations/%s/" % self.id

class Band(models.Model):
    ## attributes
    name = models.CharField(_('name'), max_length=300)
    bio = models.TextField(_('bio'), )
    pub_date = models.DateTimeField(_('date created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    ## relations
    admin = models.ForeignKey(User, editable=False)
    members = models.ManyToManyField(User, blank=True, related_name="bands", through="BandMembership")
    genres = models.ManyToManyField(MusicGenre, related_name="bands")

    def _get_stub_from_name(self):
        return self.name.tolower().replace(" ", "")
    stub = property(_get_stub_from_name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/bands/%s/" % self.id

class OrganizationMembership(models.Model):
    ## attributes
    date_joined = models.DateField(_('date Joined'), blank=True)
    position = models.CharField(_('position'), max_length=300, blank=True)

    ## relations
    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(User)

class BandMembership(models.Model):
    ## attributes
    date_joined = models.DateField(_('date Joined'), blank=True)
    position = models.CharField(_('position'), max_length=300, blank=True)

    ## relations
    band = models.ForeignKey(Band)
    user = models.ForeignKey(User)
