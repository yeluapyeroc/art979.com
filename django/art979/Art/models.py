from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from art979.Category.models import ArtistCategory, MusicGenre, FilmGenre, LiteratureGenre
from art979.Profile.models import Organization, Band
from art979.Venue.models import Venue
from art979.utils import image_path, audio_path, video_path, doc_path

class ArtPiece(models.Model):
    ## attributes ##
    title = models.CharField(_('title'), max_length=300)
    url = models.URLField(_('url'), max_length=300, blank=True)
    pub_date = models.DateTimeField(_('publication date'), 'date created', auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), 'date last modified', auto_now=True)
    image = models.ImageField(_('image'), upload_to=image_path, blank=True)
    bio = models.TextField(_('bio'))

    ## options ##
    published = models.BooleanField(_('published option'), default=False, editable=True)

    ## relations ##
    user = models.ForeignKey(User, editable=False)

    class Meta:
        abstract = True

    def _get_stub_from_title(self):
        return self.title.tolower().replace(" ", "")
    stub = property(_get_stub_from_title)

    def __unicode__(self):
        return self.title

class Album(ArtPiece):
    ## attributes
    audio = models.FileField(_('audio file'), upload_to=audio_path, blank=True)

    ## relations
    genres = models.ManyToManyField(MusicGenre, related_name='albums')
    band = models.ForeignKey(Band, blank=True, related_name='albums')

    def get_absolute_url(self):
        return "/artists/%s/albums/%s/" % (self.user.id, self.id)

class Song(ArtPiece):
    ## attributes
    length = models.CharField(_('length'), max_length=50)
    audio = models.FileField(_('audio file'), upload_to=audio_path, blank=True)

    ## relations
    genres = models.ManyToManyField(MusicGenre, related_name='songs')
    album = models.ForeignKey(Album, blank=True, related_name='songs')
    band = models.ForeignKey(Band, blank=True, related_name='songs')

    def get_absolute_url(self):
        return "/artists/%s/songs/%s/" % (self.user.id, self.id)

class VisualPiece(ArtPiece):
    ## relations
    categories = models.ManyToManyField(ArtistCategory, related_name='visual_pieces')
    venue = models.ForeignKey(Venue, blank=True, related_name='visual_pieces')

    def get_absolute_url(self):
        return "/artists/%s/visualpieces/%s/" % (self.user.id, self.id)

class LiteraturePiece(ArtPiece):
    ## attributes
    length = models.CharField(_('length'), max_length=50)

    ## relations
    genres = models.ManyToManyField(LiteratureGenre, related_name='literature_pieces')
    venue = models.ForeignKey(Venue, blank=True, related_name='literature_pieces')

    def get_absolute_url(self):
        return "/artists/%s/literaturepieces/%s/" % (self.user.id, self.id)

class Food(ArtPiece):
    ## relations
    venue = models.ForeignKey(Venue, blank=True, related_name='food')

    def get_absolute_url(self):
        return "/artists/%s/food/%s/" % (self.user.id, self.id)

class Film(ArtPiece):
    ## attributes
    length = models.CharField(_('length'), max_length=50)
    video = models.FileField(_('video File'), upload_to=video_path, blank=True)

    ## relations
    genre = models.ForeignKey(FilmGenre, related_name='films')
    venue = models.ForeignKey(Venue, blank=True, related_name='films')

    def get_absolute_url(self):
        return "/artists/%s/films/%s/" % (self.user.id, self.id)

class PerformingPiece(ArtPiece):
    ## attributes
    length = models.CharField(_('length'), max_length=50)

    ## relations
    venue = models.ForeignKey(Venue, blank=True, related_name='performing_pieces')

    def get_absolute_url(self):
        return "/artists/%s/performingpieces/%s/" % (self.user.id, self.id)
