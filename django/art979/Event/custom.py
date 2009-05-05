from django.db import models
from django import forms
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from art979 import settings

import datetime, re

EMPTY_VALUES = (None, '', [], {})

class RecurringDate(object):
    """
    Class that defines an event date that repeats at certain intervals.
    Either none, daily, weekly, monthly, or yearly.
    """
    regex = re.compile(r'(?P<start_date>\d\d?/\d\d?/\d{4}),((?P<start_time>\d\d?:\d\d)(?P<start_time_suffix>am|pm)),(?P<end_date>\d\d?/\d\d?/\d{4}),((?P<end_time>\d\d?:\d\d)(?P<end_time_suffix>am|pm)),(?P<recur_type>none|daily|weekly|monthly|yearly),?(?P<weekly_option>\d\d?,)?(?P<weekly_days>((sun|mon|tue|wed|thu|fri|sat),){,7})?(?P<monthly_option>(weekday|monthday),)?((?P<until>until|never),?(?P<until_date>\d\d?/\d\d?/\d{4})?)?')
    def __init__(self, data=None):
        self.datetimes = []
        if not data:
            duration = datetime.timedelta(hours=1)
            self.start_datetime = datetime.datetime.today()
            self.end_datetime = datetime.datetime.today() + duration
            self.db_value = "%s/%s/%s,1:00pm,%s/%s/%s,2:00pm,none" % (self.start_datetime.month, self.start_datetime.day, self.start_datetime.year, self.end_datetime.month, self.end_datetime.day, self.end_datetime.year)
        else:
            self.db_value = data
            match = self.regex.match(data)
            if not match.group(0):
                raise
            start_date = match.group('start_date').split('/')
            start_time = match.group('start_time').split(':')
            start_time_suffix = match.group('start_time_suffix')
            if start_time_suffix == 'pm' and int(start_time[0]) != 12:
                start_time[0] = int(start_time[0]) + 12
            if start_time_suffix == 'am' and int(start_time[0]) == 12:
                start_time[0] = 0
            self.start_datetime = datetime.datetime(int(start_date[2]), int(start_date[0]), int(start_date[1]), int(start_time[0]), int(start_time[1]))
            end_date = match.group('end_date').split('/')
            end_time = match.group('end_time').split(':')
            end_time_suffix = match.group('end_time_suffix')
            if end_time_suffix == 'pm' and int(end_time[0]) != 12:
                end_time[0] = int(end_time[0]) + 12
            if end_time_suffix == 'am' and int(end_time[0]) == 12:
                end_time[0] = 0
            self.end_datetime = datetime.datetime(int(end_date[2]), int(end_date[0]), int(end_date[1]), int(end_time[0]), int(end_time[1]))
            self.recur_type = match.group('recur_type')
            self.weekly_option = match.group('weekly_option')
            self.weekly_days = match.group('weekly_days')
            self.monthly_option = match.group('monthly_option')
            self.until = match.group('until')
            until_date = match.group('until_date').split('/')
            self.until_date = datetime.date(int(until_date[2]), int(until_date[0]), int(until_date[1]))

    def __unicode__(self):
        return self.db_value

    def __lt__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime < other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime < other.start_datetime:
                return True
            else:
                return False

    def __le__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime <= other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime <= other.start_datetime:
                return True
            else:
                return False

    def __eq__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime == other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime == other.start_datetime:
                return True
            else:
                return False

    def __ne__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime != other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime != other.start_datetime:
                return True
            else:
                return False

    def __gt__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime > other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime > other.start_datetime:
                return True
            else:
                return False

    def __ge__(self, other):
        if other.__name__ == "datetime":
            if self.start_datetime >= other:
                return True
            else:
                return False
        if other.__name__ == "RecurringDate":
            if self.start_datetime >= other.start_datetime:
                return True
            else:
                return False

class RecurringDateInput(forms.widgets.Input):
    class Media:
        js = (
            'js/jquery-1.3.2.js',
            'js/recurringdate.js',
        )
        css = {
                'screen, projection': ('css/recurringdate.css',)
                }

    def __init__(self, attrs=None):
        super(RecurringDateInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value=''
        return mark_safe(u'<div class="recurringDateInput"%s><input%s /></div>' % (flatatt(dict(rel=name)), flatatt(dict(name=name, rel=u'value', type=u'hidden', value=force_unicode(value)))))

class RecurringDateFormField(forms.Field):
    widget = RecurringDateInput
    default_error_messages = {
            'invalid': _('Please do not alter your headers.'),
            }

    def __init__(self, *args, **kwargs):
        super(RecurringDateFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(RecurringDateFormField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        try:
            check_value = value.split(',')
        except:
            raise forms.ValidationError(self.error_messages['invalid'])
        regex = re.compile(r'(?P<start_date>\d\d?/\d\d?/\d{4}),((?P<start_time>\d\d?:\d\d)(?P<start_time_suffix>am|pm)),(?P<end_date>\d\d?/\d\d?/\d{4}),((?P<end_time>\d\d?:\d\d)(?P<end_time_suffix>am|pm)),(?P<recur_type>none|daily|weekly|monthly|yearly),?(?P<weekly_option>\d\d?,)?(?P<weekly_days>((sun|mon|tue|wed|thu|fri|sat),){,7})?(?P<monthly_option>(weekday|monthday),)?((?P<until>until|never),?(?P<until_date>\d\d?/\d\d?/\d{4})?)?')
        match = regex.match(value)
        if not match.group(0):
            raise forms.ValidationError(self.error_messages['invalid'])
        start_date = match.group('start_date').split('/')
        start_time = match.group('start_time').split(':')
        start_time_suffix = match.group('start_time_suffix')
        if start_time_suffix == 'pm' and int(start_time[0]) != 12:
            start_time[0] = int(start_time[0]) + 12
        if start_time_suffix == 'am' and int(start_time[0]) == 12:
            start_time[0] = 0
        start_datetime = datetime.datetime(int(start_date[2]), int(start_date[0]), int(start_date[1]), int(start_time[0]), int(start_time[1]))
        end_date = match.group('end_date').split('/')
        end_time = match.group('end_time').split(':')
        end_time_suffix = match.group('end_time_suffix')
        if end_time_suffix == 'pm' and int(end_time[0]) != 12:
            end_time[0] = int(end_time[0]) + 12
        if end_time_suffix == 'am' and int(end_time[0]) == 12:
            end_time[0] = 0
        end_datetime = datetime.datetime(int(end_date[2]), int(end_date[0]), int(end_date[1]), int(end_time[0]), int(end_time[1]))
        if end_datetime < start_datetime:
            raise forms.ValidationError("The event's start date/time must come before the end date/time")
        until_date = match.group('until_date').split('/')
        until_date = datetime.datetime(int(until_date[2]), int(until_date[0]), int(until_date[1]), int(start_time[0]), int(start_time[1]))
        if until_date and until_date < start_datetime:
            raise forms.ValidationError("The event's until date must come after the start date/time")
        return value

class RecurringDateField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(RecurringDateField, self).__init__(*args, **kwargs)

    def db_type(self):
        return "char(100)"

    def to_python(self, value):
        if isinstance(value, RecurringDate):
            return value
        return RecurringDate(value)

    def get_db_prep_value(self, value):
        return value.db_value

    def formfield(self, **kwargs):
        defaults = {'form_class': RecurringDateFormField}
        defaults.update(kwargs)
        return super(RecurringDateField, self).formfield(**defaults)
