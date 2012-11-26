from django.db import models
from django.contrib.auth.models import User
from member.models import Person

from datetime import datetime, time, timedelta

EMD078_TYPE = (
    ('mission', 'Mission'),
    ('training', 'Training'),
)


class MissionCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_mission = models.BooleanField(help_text='Should sign-ins in this '
        'category count toward mission hours.')
    is_training = models.BooleanField(help_text='Should sign-ins in this '
        'category count toward training hours.')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'mission categories'


class Mission(models.Model):
    mission_number = models.CharField(max_length=20, unique=True)
    mission_type = models.CharField(max_length=40, choices=EMD078_TYPE,
        null=True, blank=True, help_text='EMD-078 mission type')
    category = models.ForeignKey(MissionCategory,
        help_text='PCESAR internal tracking category.')
    mission_name = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=60)
    date_start = models.DateField()
    date_end = models.DateField()
    signed_in = models.ManyToManyField(Person, through='Signin')
    signed = models.CharField(max_length=255, blank=True,
        help_text="This form must be signed by local emergency management "
        "director/coordinator or sheriff's deputy.")
    prepared_by = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        if self.mission_name:
            return u'%s (%s)' % (self.mission_number, self.mission_name)
        return self.mission_number

    def total_hours(self):
        return self.signin_set.aggregate(models.Sum('hours'))['hours__sum']

    def total_miles(self):
        return self.signin_set.aggregate(models.Sum('miles_driven'))['miles_driven__sum']


class Signin(models.Model):
    mission = models.ForeignKey(Mission)
    person = models.ForeignKey(Person)
    assignment = models.CharField(max_length=16, blank=True)
    time1_in = models.TimeField(null=True, blank=True)
    time1_out = models.TimeField(null=True, blank=True)
    time2_in = models.TimeField(null=True, blank=True)
    time2_out = models.TimeField(null=True, blank=True)
    time3_in = models.TimeField(null=True, blank=True)
    time3_out = models.TimeField(null=True, blank=True)
    hours = models.FloatField(editable=False)
    miles_driven = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s @ %s' % (self.person, self.mission)

    def clean(self):
        from django.core.exceptions import ValidationError

        date_start = self.mission.date_start

        # convert to datetimes before comparison
        time1_in = datetime.combine(date_start, self.time1_in or time())
        if self.time1_out is None:
            time1_out = datetime.combine(date_start + timedelta(days=1), time())
        else:
            time1_out = datetime.combine(date_start, self.time1_out)

        time2_in = datetime.combine(date_start + timedelta(days=1),
            self.time2_in or time())
        if self.time2_out is None:
            time2_out = datetime.combine(date_start + timedelta(days=2), time())
        else:
            time2_out = datetime.combine(date_start + timedelta(days=1), self.time2_out)

        time3_in = datetime.combine(date_start + timedelta(days=2),
            self.time2_in or time())
        if self.time3_out is None:
            time3_out = datetime.combine(date_start + timedelta(days=3), time())
        else:
            time3_out = datetime.combine(date_start + timedelta(days=2), self.time3_out)

        if time1_in > time1_out:
            raise ValidationError('Time Out must be later than Time In.')
        if time2_in > time2_out:
            raise ValidationError('Time Out must be later than Time In.')
        if time3_in > time3_out:
            raise ValidationError('Time Out must be later than Time In.')

    def calc_hours(self):
        date_start = self.mission.date_start

        # convert to datetimes before comparison
        time1_in = datetime.combine(date_start, self.time1_in or time())
        if self.time1_out is None:
            time1_out = datetime.combine(date_start + timedelta(days=1), time())
        else:
            time1_out = datetime.combine(date_start, self.time1_out)

        time2_in = datetime.combine(date_start + timedelta(days=1),
            self.time2_in or time())
        if self.time2_out is None:
            time2_out = datetime.combine(date_start + timedelta(days=2), time())
        else:
            time2_out = datetime.combine(date_start + timedelta(days=1), self.time2_out)

        time3_in = datetime.combine(date_start + timedelta(days=2),
            self.time2_in or time())
        if self.time3_out is None:
            time3_out = datetime.combine(date_start + timedelta(days=3), time())
        else:
            time3_out = datetime.combine(date_start + timedelta(days=2), self.time3_out)

        duration = timedelta()
        if self.time1_in is not None:
            duration += time1_out - time1_in
        if self.time2_out is None:
            if self.time3_in is None and self.time3_out is not None:
                duration += timedelta(hours=24)
        else:
            duration += time2_out - time2_in
        if self.time3_out is not None:
            duration += time3_out - time3_in
        return duration.days * 24 + duration.seconds / 3600.

    def save(self, *args, **kwargs):
        self.hours = self.calc_hours()
        super(Signin, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Sign-in'
