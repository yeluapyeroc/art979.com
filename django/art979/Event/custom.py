from django.db import models
from django import forms
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

EMPTY_VALUES = (None, '')

class WeeklyRecur(object):
    def __init__(self, days=[]):
        self.days = days

    def _get_db_value(self):
        return ''.join([','.join(l) for l in days])
    db_value = property(_get_db_value)

class MonthlyRecur(object):
    def __init__(self):
        self.data = []

    def add_recur(self, which='', day=''):
        self.data.append([which, day])

    def _get_db_value(self):
        temp = []
        for l in self.data:
            temp.append(','.join(l[0], l[1]))
        return ''.join([''.join(l) for l in temp])
    db_value = property(_get_db_value)

class WeeklyRecurringDateInput(forms.widgets.Input):
    def __init__(self, attrs=None):
        super(WeeklyRecurringDateInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        if value is None: value='tue,mon'
        return mark_safe(u'\n<div class="weeklydate"%s>\n' % flatatt(dict(rel=name)) + u'\n'.join([(u'<button class="dayButton"%s>%s</button>\n<input%s />' % (flatatt(dict(type=u'button', rel=force_unicode(d))), force_unicode(d), flatatt(dict(rel=force_unicode(d), type=u'hidden', value=u'unpressed')))) for d in DAYS]) + u'\n<input%s />\n</div>' % flatatt(dict(name=name, type=u'hidden', value=force_unicode(value), id=u'weeklydatevalue')))

class WeeklyRecurringDateFormField(forms.Field):
    widget = WeeklyRecurringDateInput
    default_error_messages = {
        'invalid': _(u'Please do not alter your headers.'),
    }

    def __init__(self, *args, **kwargs):
        super(WeeklyRecurringDateFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        super(WeeklyRecurringDateFormField, self).clean(value)
        if value in EMPTY_Values:
            return ''
        try:
            check_value = value.split(',')
        except:
            raise ValidationError(self.error_messages['invalid'])
        for v in check_value:
            if v not in DAYS:
                raise ValidationError(self.error_messages['invalid'])
        return value

class MonthlyRecurringDateFormField(forms.Field):
    pass

class WeeklyRecurringDateField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.max_length = 15
        self.default = WeeklyRecur()
        super(WeeklyRecurringDateField, self).__init__(*args, **kwargs)

    def db_type(self):
        return 'char(%s)' % self.max_length

    def to_python(self, value):
        if isinstance(value, WeeklyRecur):
            return Value
        days = value.split(',')
        return WeeklyRecur(days)

    def get_db_prep_value(self, value):
        return value.db_value

    def formfield(self, **kwargs):
        defaults = {'form_class': WeeklyRecurringDateFormField}
        defaults.update(kwargs)
        return super(WeeklyRecurringDateField, self).formfield(**defaults)

class MonthlyRecurringDateField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.max_length = 250
        self.default = MonthlyRecur()
        super(MonthlyRecurringDateField, self).__init__(*args, **kwargs)

    def db_type(self):
        return 'char(%s)' % self.max_length

    def to_python(self, value):
        if isinstance(value, MonthlyRecur):
            return value
        data = value.split(',')
        recur = MonthlyRecur()
        while len(data) > 0:
            recur.add_recur(data.pop(0), data.pop(0))
        return recur

    def get_db_prep_value(self, value):
        return value.db_value

    def formfield(self, **kwargs):
        defaults = {'form_class': MonthlyRecurringDateFormField}
        defaults.update(kwargs)
        return super(MonthlyRecurringDateField, self).formfield(**defaults)
