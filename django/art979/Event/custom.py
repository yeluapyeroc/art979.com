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
    def __init__(self, data=[]):
        self.data = data

    def _get_db_value(self):
        return ','.join(self.data)
    db_value = property(_get_db_value)

    def __unicode__(self):
        return ','.join(self.data)

class RecurringDateInput(forms.widgets.Input):
    class Media:
        js = (
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
            raise ValidationError(self.error_messages['invalid'])
        regex = re.compile(r'(?P<start_date>\d{4},\d\d?,\d\d?),(?P<start_time>\d\d?:\d\d(?P<start_time_suffix>am|pm)),(?P<end_date>\d{4},\d\d?,\d\d?),(?P<end_time>\d\d?:\d\d(?P<end_time_suffix>am|pm)),(?P<recur_type>none|daily|weekly|monthly|yearly),(?P<weekly_option>\d\d?,)?(?P<weekly_days>((sun|mon|tue|wed|thu|fri|sat),){,7})?(?P<monthly_option>(weekday|monthday),)?(?P<until_date>until,(\d{4},\d\d?,\d\d?)|never)?')
        if not regex.match(value):
            raise ValidationError(self.error_messages['invalid'])
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
        return RecurringDate(value.split(','))

    def get_db_prep_value(self, value):
        return value.db_value

    def formfield(self, **kwargs):
        defaults = {'form_class': RecurringDateFormField}
        defaults.update(kwargs)
        return super(RecurringDateField, self).formfield(**defaults)
