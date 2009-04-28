from django.db import models
from django.contrib.auth.models import User
from art979.Venue.models import Venue
from art979.Event.models import Event
from art979.Profile.models import Band, Organization
from art979.Art.models import Album, Song, VisualPiece, PerformingPiece, LiteraturePiece, Food, Film

class Story(models.Model):
    ## globals ##
    SUBJECT_CHOICES = (
        ('music', 'Music'),
        ('visual', 'Visual Arts'),
        ('culinary', 'Culinary Arts'),
        ('literary', 'Literary Arts'),
        ('artisan', 'Artisan'),
        ('design', 'Design'),
        ('performing', 'Performing Arts'),
        ('other', 'Other'),
    )

    ## attributes ##
    headline = models.CharField(max_length=300)
    body = models.TextField()
    pub_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('date last modified', auto_now=True, editable=False)
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)

    ## images and captions ##
    image1 = models.ImageField(upload_to='img/story/', blank=True)
    image2 = models.ImageField(upload_to='img/story/', blank=True)
    image3 = models.ImageField(upload_to='img/story/', blank=True)
    image4 = models.ImageField(upload_to='img/story/', blank=True)
    image5 = models.ImageField(upload_to='img/story/', blank=True)
    caption1 = models.CharField(max_length=450, blank=True)
    caption2 = models.CharField(max_length=450, blank=True)
    caption3 = models.CharField(max_length=450, blank=True)
    caption4 = models.CharField(max_length=450, blank=True)
    caption5 = models.CharField(max_length=450, blank=True)

    ## options ##
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False, editable=False)

    ## relations ##
    user = models.ForeignKey(User)
    venues = models.ManyToManyField(Venue, blank=True, related_name="stories")
    artists = models.ManyToManyField(User, blank=True, related_name="stories")
    bands = models.ManyToManyField(Band, blank=True, related_name="stories")
    organizations = models.ManyToManyField(Organization, blank=True, related_name="stories")
    albums = models.ManyToManyField(Album, blank=True, related_name="stories")
    songs = models.ManyToManyField(Song, blank=True, related_name="stories")
    visual_pieces = models.ManyToManyField(VisualPiece, blank=True, related_name="stories")
    literature_pieces = models.ManyToManyField(LiteraturePiece, blank=True, related_name="stories")
    entrees = models.ManyToManyField(Food, blank=True, related_name="stories")
    films = models.ManyToManyField(Film, blank=True, related_name="stories")
    performing_pieces = models.ManyToManyField(PerformingPiece, blank=True, related_name="stories")

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    def _get_stub_from_headline(self):
        return self.headline.tolower().replace(" ", "")
    stub = property(_get_stub_from_headline)

    def get_absolute_url(self):
        return "/stories/%s/" % self.id

    def __unicode__(self):
        return self.stub

class Update(models.Model):
    ## attributes ##
    title = models.CharField(max_length=150)
    body = models.TextField()
    pub_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('date last modified', auto_now=True, editable=False)

    ## options ##
    published = models.BooleanField(default=False, editable=False)

    ## relations ##
    venue = models.ForeignKey(Venue, editable=False, related_name="updates")

    class Meta:
        verbose_name = "Update"
        verbose_name_plural = "Updates"

    def get_absolute_url(self):
        return "/venues/%s/" % self.venue.id

    def __unicode__(self):
        return "%s update %s" % (self.venue.name, self.id)
