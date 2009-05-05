from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from art979.Event.models import Event
from art979.Event.forms import CreateEventForm
from art979.Category.models import EventType
from art979.Story.models import Story
from art979.Profile.forms import RegisterForm

import datetime, re

def home(request):
    stories = Story.objects.all().order_by('pub_date')[1:9]
    feature = Story.objects.all().order_by('pub_date')[0]
    return render_to_response('home.html', {'stories': stories, 'feature': feature}, context_instance=RequestContext(request))

def gallery(request):
    return render_to_response('gallery.html', {}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
    else:
        form = RegisterForm()
    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

def story(request, story_id):
    return render_to_response('story.html', {}, context_instance=RequestContext(request))

def category(request, category):
    stories = Story.objects.filter(subject=category).order_by('pub_date')[1:9]
    feature = Story.objects.filter(subject=category).order_by('pub_date')[0]
    return render_to_response('category.html', {'stories': stories, 'feature': feature}, context_instance=RequestContext(request))

def artist_category(request, category, artist_category):
    return render_to_response('category.html', {}, context_instance=RequestContext(request))

def music_genre(request, genre_id):
    return render_to_response('music_genre.html', {}, context_instance=RequestContext(request))

def film_genre(request, genre_id):
    return render_to_response('film_genre.html', {}, context_instance=RequestContext(request))

def literature_genre(request, genre_id):
    return render_to_response('literature_genre.html', {}, context_instance=RequestContext(request))

def events(request, event_type=None):
    return render_to_response('events.html', {}, context_instance=RequestContext(request))

def event_profile(request, event_id):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def venues(request, venue_type=None):
    return render_to_response('venues.html', {}, context_instance=RequestContext(request))

def venue_profile(request, venue_id):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def artist_profile(request, artist_id):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def artist_art(request, artist_id, art_type):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def art_profile(request, artist_id, art_type, art_id):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def bands(request):
    return render_to_response('groups.html', {}, context_instance=RequestContext(request))

def band_profile(request, band_id):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def organizations(request):
    return render_to_response('groups.html', {}, context_instance=RequestContext(request))

def organization_profile(request):
    return render_to_response('profile.html', {}, context_instance=RequestContext(request))

def account(request):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def account_options(request):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def account_delete(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def model_create(request, model_type, art_type=None):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def model_edit(request, model_type, art_type=None, art_id=None, model_id=None):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def model_delete(request, model_type, art_type=None, art_id=None, model_id=None):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def model_get(request, model_type, art_type=None, art_id=None, model_id=None):
    return render_to_response('account.html', {}, context_instance=RequestContext(request))

def test(request):
    if request.method == "POST":
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            form.save_m2m()
            return HttpResponseRedirect('/')
    else:
        form = CreateEventForm()

    return render_to_response('test.html', {'form': form}, context_instance=RequestContext(request))

def verify_email(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def activate(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))
