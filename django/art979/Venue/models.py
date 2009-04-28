from django.db import models
from django.contrib.auth.models import User
from art979.Category.models import VenueType
from art979.utils import image_path

class Venue(models.Model):
    ## attributes
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    image = models.ImageField(upload_to=image_path, blank=True)
    email = models.EmailField(max_length=100)
    pub_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('date last modified', auto_now=True, editable=False)
    url = models.URLField(blank=True)
    bio = models.TextField()

    ## relations
    user = models.ForeignKey(User)
    type = models.ManyToManyField(VenueType, related_name='venues')

    def _get_stub_from_name(self):
        return self.name.tolower().replace(" ", "")
    stub = property(_get_stub_from_name)

    def get_absolute_url(self):
        return "/venues/%s/" % (self.id)
