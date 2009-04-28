from django.db import models

class CategoryBase(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100, blank=True, help_text='Should be capitalized.')
    description = models.TextField()
    pub_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('date last modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

    def _get_stub_from_name(self):
        return self.name.tolower().replace(" ", "")
    stub = property(_get_stub_from_name)

class ArtistCategory(CategoryBase):
    SUBJECT_CHOICES = (
        ('visual', 'Visual Arts'),
        ('music', 'Music'),
        ('culinary', 'Culinary Arts'),
        ('literary', 'Literary Arts'),
        ('artisan', 'Artisan'),
        ('design', 'Design'),
        ('performing', 'Performing Arts'),
    )

    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    art_noun = models.CharField(max_length=100, help_text='Noun to display for art pieces in this category.')

    class Meta:
        verbose_name = 'Artist Category'
        verbose_name_plural = 'Artist Categories'

    def get_absolute_url(self):
        return "/%s/%s/" % (self.subject, self.stub)

    def __unicode__(self):
        return self.name

class MusicGenre(CategoryBase):
    ## attributes
    subject = 'music'

    class Meta:
        verbose_name = 'Music Genre'
        verbose_name_plural = 'Music Genres'

    def get_absolute_url(self):
        return "/music/genres/%s/" % self.id

    def __unicode__(self):
        return "Music | %s" % self.name

class FilmGenre(CategoryBase):
    ## attributes
    subject = 'visual'
    
    class Meta:
        verbose_name = 'Film Genre'
        verbose_name_plural = 'Film Genres'

    def get_absolute_url(self):
        return "/film/genres/%s/" % self.id

    def __unicode__(self):
        return "Film | %s" % self.name

class LiteratureGenre(CategoryBase):
    ## attributes
    subject = 'literary'

    class Meta:
        verbose_name = 'Literature Genre'
        verbose_name_plural = 'Literature Genres'

    def get_absolute_url(self):
        return "/literary/genres/%s/" % self.id

    def __unicode__(self):
        return "Literature | %s" % self.name

class VenueType(CategoryBase):
    class Meta:
        verbose_name = 'Venue Type'
        verbose_name_plural = 'Venue Types'

    def get_absolute_url(self):
        return "/venues/%s/" % self.stub

    def __unicode__(self):
        return "Venue | %s" % self.name

class EventType(CategoryBase):
    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'

    def get_absolute_url(self):
        return "/events/%s/" % self.stub

    def __unicode__(self):
        return "Event | %s" % self.name
