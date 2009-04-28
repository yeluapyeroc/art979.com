from django.conf.urls.defaults import *
from django.contrib import admin

from art979.feeds import EventsFeed, StoriesFeed, VenueUpdatesFeed

admin.autodiscover()

feeds = {
    'events': EventsFeed,
    'stories': StoriesFeed,
    'venueupdates': VenueUpdatesFeed,
}

urlpatterns = patterns('',
## Static Media Serving ##
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/media/Storage/programming/web/art979.com/httpdocs/media'}),

## Extras ##
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('art979.Page.views',

## Administration Urls ##
    (r'^thanks/$', 'thanks'),
    (r'^activate/$', 'activate'),
    (r'^verifyemail/$', 'verify_email'),

## Category Urls ##
    (r'^music/genres/(?P<genre_id>.*)/$', 'music_genre'),
    (r'^film/genres/(?P<genre_id>.*)/$', 'film_genre'),
    (r'^literary/genres/(?P<genre_id>.*)/$', 'literature_genre'),
    (r'^(?P<category>visual|music|culinary|literary|artisan|design|performing)/$', 'category'),
    (r'^(?P<category>visual|music|culinary|literary|artisan|design|performing)/(?P<artist_category>.*)/$', 'artist_category'),

## Flat Urls ##
    (r'^gallery/$', 'gallery'),
    (r'^events/$', 'events'),
    (r'^register/$', 'register'),
    (r'^test/$', 'test'),

## Story Urls ##
    (r'^stories/(?P<story_id>\d*)/$', 'story'),

## Event Urls ##
    (r'^events/(?P<event_id>\d*)/$', 'event_profile'),
    (r'^events/(?P<event_type>.*)/$', 'events'),

## Venue Urls ##
    (r'^venues/(?P<venue_id>\d*)/$', 'venue_profile'),
    (r'^venues/(?P<venue_type>.*)/$', 'venues'),

## Artist Urls ##
    (r'^artists/(?P<artist_id>\d*)/(?P<art_type>all|songs|albums|visualpieces|food|films|literaturepieces|performingpieces)/$', 'artist_art'),
    (r'^artists/(?P<artist_id>\d*)/(?P<art_type>songs|albums|visualpieces|food|films|literaturepieces|performingpieces)/(?P<art_id>\d*)/$', 'art_profile'),
    (r'^artists/(?P<artist_id>\d*)/$', 'artist_profile'),

## Group Urls ##
    (r'^bands/(?P<band_id>\d*)/$', 'band_profile'),
    (r'^bands/$', 'bands'),
    (r'^organizations/(?P<organization_id>\d*)/$', 'organization_profile'),
    (r'^organizations/$', 'organizations'),

## Account Urls ##
    (r'^account/create/(?P<model_type>art|event|venue|story|band|organization)/(\b|(?P<art_type>song|album|visualpiece|food|film|literaturepiece|performingpiece)/)$', 'model_create'),
    (r'^account/edit/(?P<model_type>art|event|venue|story|band|organization)/((?P<art_type>song|album|visualpiece|food|film|literaturepiece|performingpiece)/(?P<art_id>\d*)|(?P<model_id>\d*))/$', 'model_edit'),
    (r'^account/delete/(?P<model_type>art|event|venue|story|band|organization)/((?P<art_type>song|album|visualpiece|food|film|literaturepiece|performingpiece)/(?P<art_id>\d*)|(?P<model_id>\d*))/$', 'model_delete'),
    (r'^account/get/(?P<model_type>all|art|event|venue|story|band|organization)/(\b|(?P<art_type>song|album|visualpiece|food|film|literaturepiece|performingpiece)/(?P<art_id>\d*)|(?P<model_id>\d*))/$', 'model_get'),
    (r'^account/options/$', 'account_options'),
    (r'^account/$', 'account'),
    (r'^deleteaccount/$', 'account_delete'),

## Home/Admin ##
    (r'^$', 'home'),
    (r'^admin/(.*)', admin.site.root),
)
