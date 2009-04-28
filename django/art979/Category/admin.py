from django.contrib import admin
from art979.Category.models import ArtistCategory, MusicGenre, LiteratureGenre, FilmGenre, VenueType, EventType

admin.site.register(ArtistCategory)
admin.site.register(VenueType)
admin.site.register(MusicGenre)
admin.site.register(LiteratureGenre)
admin.site.register(FilmGenre)
admin.site.register(EventType)
