from django.db import models
from django.contrib.auth.models import User

from art979.Venue.models import Venue
from art979.Event.models import Event
from art979.Profile.models import Band, Organization
from art979.Art.models import Album, Song, VisualPiece, PerformingPiece, LiteraturePiece, Food, Film

import Image, re

def image_regexrpl_lg(matchobj):
    if matchobj.group(0) == '.jpg': return '_lg.jpg'
    if matchobj.group(0) == '.jpeg': return '_lg.jpeg'
    if matchobj.group(0) == '.gif': return '_lg.gif'
    if matchobj.group(0) == '.png': return '_lg.png'
    return matchobj.group(0)

def image_regexrpl_md(matchobj):
    if matchobj.group(0) == '.jpg': return '_md.jpg'
    if matchobj.group(0) == '.jpeg': return '_md.jpeg'
    if matchobj.group(0) == '.gif': return '_md.gif'
    if matchobj.group(0) == '.png': return '_md.png'
    return matchobj.group(0)

def image_regexrpl_sm(matchobj):
    if matchobj.group(0) == '.jpg': return '_sm.jpg'
    if matchobj.group(0) == '.jpeg': return '_sm.jpeg'
    if matchobj.group(0) == '.gif': return '_sm.gif'
    if matchobj.group(0) == '.png': return '_sm.png'
    return matchobj.group(0)

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

    CROP_CHOICES = (
        ('top', 'Top'),
        ('bot', 'Bottom'),
        ('mid', 'Middle'),
    )

    ## attributes ##
    headline = models.CharField(max_length=300)
    body = models.TextField()
    pub_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('date last modified', auto_now=True, editable=False)
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)

    ## images and captions ##
    image = models.ImageField(upload_to='img/story/', blank=True)
    crop_option = models.CharField(max_length=3, choices=CROP_CHOICES, blank=True, default='mid')
    image_extra = models.ImageField(upload_to='img/story/', blank=True)

    ## options ##
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False, editable=False)

    ## relations ##
    user = models.ForeignKey(User)
    venues = models.ManyToManyField(Venue, blank=True, related_name="stories")
    events = models.ManyToManyField(Event, blank=True, related_name="stories")
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
        return self.headline.lower().replace(" ", "")
    stub = property(_get_stub_from_headline)

    def get_absolute_url(self):
        return "/stories/%s/" % self.id

    def __unicode__(self):
        return self.stub

    def _get_large_image(self):
        img_path = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_lg, self.image.path)
        img_url = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_lg, self.image.url)
        try:
            img = Image.open(img_path)
            return img_url
        except IOError:
            dst_width, dst_height = 950, 300
            if self.crop_option == 'top':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, 0, dst_width, int(new_height-crop_height)))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'mid' or self.crop_option == None or self.crop_option == '':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, int(crop_height/2), dst_width, int(new_height-(crop_height/2))))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'bot':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, crop_height, dst_width, new_height))
                        img.save(img_path)
                except IOError:
                    raise

        return img_url
    image_lg = property(_get_large_image)

    def _get_medium_image(self):
        img_path = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_md, self.image.path)
        img_url = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_md, self.image.url)
        try:
            img = Image.open(img_path)
            return img_url
        except IOError:
            dst_width, dst_height = 470, 235
            if self.crop_option == 'top':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, 0, dst_width, int(new_height-crop_height)))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'mid':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, int(crop_height/2), dst_width, int(new_height-(crop_height/2))))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'bot':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, crop_height, dst_width, new_height))
                        img.save(img_path)
                except IOError:
                    raise

        return img_url
    image_md = property(_get_medium_image)

    def _get_small_image(self):
        img_path = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_sm, self.image.path)
        img_url = re.sub(r'\.(jpg|jpeg|gif|png)$', image_regexrpl_sm, self.image.url)
        try:
            img = Image.open(img_path)
            return img_url
        except IOError:
            dst_width, dst_height = 230, 115
            if self.crop_option == 'top':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, 0, dst_width, int(new_height-crop_height)))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'mid':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, int(crop_height/2), dst_width, int(new_height-(crop_height/2))))
                        img.save(img_path)
                except IOError:
                    raise
    
            if self.crop_option == 'bot':
                try:
                    img = Image.open(self.image.path)
                    src_width, src_height = img.size
                    src_ratio = float(src_width) / float(src_height)
                    dst_ratio = float(dst_width) / float(dst_height)
                    new_height = int(float(dst_width) / float(src_ratio))
                    img = img.resize((dst_width, new_height), Image.ANTIALIAS)
                    if new_height < dst_height:
                        img.save(img_path)
                    else:
                        crop_height = int(new_height) - int(dst_height)
                        img = img.crop((0, crop_height, dst_width, new_height))
                        img.save(img_path)
                except IOError:
                    raise

        return img_url
    image_sm = property(_get_small_image)

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
