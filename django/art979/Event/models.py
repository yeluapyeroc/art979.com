from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from art979.Category.models import EventType
from art979.Profile.models import Band
from art979.Art.models import Album, Song, LiteraturePiece, VisualPiece, Film, Food, PerformingPiece
from art979.Venue.models import Venue
from art979.utils import image_path
from art979.Event.custom import RecurringDateField

class Event(models.Model):
    """
    An event that can reference a venue it takes place at, multiple artsists/bands/organizations,
    multiple art pieces, and users that are following it.

    # Create some events
    >>> concert = Event.objects.create(name="concert", url="http://art979.com/")

    """
    ## attributes
    name = models.CharField(_('name'), max_length=300)
    url = models.URLField(_('url'), blank=True)
    image = models.ImageField(_('image'), upload_to=image_path, blank=True)
    date = RecurringDateField(_('Date'), blank=True)
    pub_date = models.DateTimeField(_('publication date'), 'date created', auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), 'date last modified', auto_now=True)
    ticket_prices = models.CharField(_('ticket prices'), max_length=75, blank=True)
    bio = models.TextField(_('bio'), blank=True)

    ## options ##
    published = models.BooleanField(_('published option'), default=False, editable=True)

    ## relations
    user = models.ForeignKey(User, editable=False)
    type = models.ForeignKey(EventType, related_name='events')
    venue = models.ForeignKey(Venue, blank=True, null=True, related_name='events')
    artists = models.ManyToManyField(User, blank=True, null=True, related_name='events')
    bands = models.ManyToManyField(Band, blank=True, null=True, related_name='events')
    albums = models.ManyToManyField(Album, blank=True, null=True, related_name='events')
    songs = models.ManyToManyField(Song, blank=True, null=True, related_name='events')
    performing_pieces = models.ManyToManyField(PerformingPiece, blank=True, null=True, related_name='events')
    visual_pieces = models.ManyToManyField(VisualPiece, blank=True, null=True, related_name='events')
    literature_pieces = models.ManyToManyField(LiteraturePiece, blank=True, null=True, related_name='events')
    films = models.ManyToManyField(Film, blank=True, null=True, related_name='events')
    food = models.ManyToManyField(Food, blank=True, null=True, related_name='events')
    followers = models.ManyToManyField(User, blank=True, null=True, related_name='followed_events')

    def _get_stub_from_name(self):
        return self.name.tolower().replace(" ", "")
    stub = property(_get_stub_from_name)

    def get_absolute_url(self):
        return "/events/%s/" % (self.id)

    def __unicode__(self):
        return self.name
