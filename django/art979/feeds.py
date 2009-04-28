from django.contrib.syndication.feeds import FeedDoesNotExist, Feed
from django.core.exceptions import ObjectDoesNotExist

from art979.Category.models import EventType
from art979.Event.models import Event
from art979.Story.models import Story
from art979.Venue.models import Venue

class EventsFeed(Feed):
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        elif len(bits) == 0:
            return None
        return EventType.objects.get(stub=bits[0])

    def title(self, obj):
        if not obj:
            return "Art979 | Events"
        return "Art979 | Events | %s" % (obj.plural)

    def link(self, obj):
        if not obj:
            return "http://art979.com/events/"
        return "http://art979.com/events/%s/" % (obj.stub)

    def description(self, obj):
        if not obj:
            return "Upcoming Events"
        return "Upcoming %s" % (obj.plural)

    def items(self, obj):
        if not obj:
            return Event.objects.all().order_by('start_date')
        return Event.objects.filter(type__id=obj.id)

class StoriesFeed(Feed):
    """
    Art979 Stories RSS Feed
    """
    title = "Art979 | Stories"
    link = "http://art979.com/"
    description = "Stories from Art979.com"

    def items(self):
        return Story.objects.filter(published=True).order_by('pub_date')

class VenueUpdatesFeed(Feed):
    """
    Feed for individual venue's updates
    """
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Venue.objects.get(id=bits[0])

    def title(self, obj):
        return "%s Updates" % obj.name

    def link(self, obj):
        return "http://art979.com/venues/%s/" % obj.id

    def description(self, obj):
        return "Updates for %s" % obj.name

    def items(self, obj):
        return obj.updates.all().order_by('pub_date')
