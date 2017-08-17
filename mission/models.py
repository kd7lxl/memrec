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
    day1 = models.DateField()
    day2 = models.DateField(null=True, blank=True)
    day3 = models.DateField(null=True, blank=True)
    total_personnel = models.PositiveIntegerField(default=0)
    total_hours = models.FloatField()
    total_miles = models.PositiveIntegerField(default=0)
    signed_in = models.ManyToManyField(Person, through='Signin')
    signed = models.CharField(max_length=255, null=True, blank=True,
        help_text="This form must be signed by local emergency management "
        "director/coordinator or sheriff's deputy.")
    prepared_by = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        if self.mission_name:
            return u'%s %s' % (self.mission_number, self.mission_name)
        return self.mission_number

    class Meta:
        ordering = ['-date_start']


class Signin(models.Model):
    mission = models.ForeignKey(Mission)
    person = models.ForeignKey(Person)
    assignment = models.CharField(max_length=16, blank=True)
    time1_in = models.DateTimeField(null=True, blank=True)
    time1_out = models.DateTimeField(null=True, blank=True)
    time2_in = models.DateTimeField(null=True, blank=True)
    time2_out = models.DateTimeField(null=True, blank=True)
    time3_in = models.DateTimeField(null=True, blank=True)
    time3_out = models.DateTimeField(null=True, blank=True)
    hours = models.FloatField(editable=False)
    miles_driven = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return u'%s @ %s' % (self.person, self.mission)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.time1_in > self.time1_out:
            raise ValidationError('Time Out must be later than Time In.')
        if self.time2_in > self.time2_out:
            raise ValidationError('Time Out must be later than Time In.')
        if self.time3_in > self.time3_out:
            raise ValidationError('Time Out must be later than Time In.')

    def calc_hours(self):
        duration = timedelta()
        if self.time1_in is not None:
            duration += self.time1_out - self.time1_in
        if self.time2_out is None:
            if self.time3_in is None and self.time3_out is not None:
                duration += timedelta(hours=24)
        else:
            duration += self.time2_out - self.time2_in
        if self.time3_out is not None:
            duration += self.time3_out - self.time3_in
        return duration.days * 24 + duration.seconds / 3600.

    def save(self, *args, **kwargs):
        self.hours = self.calc_hours()
        super(Signin, self).save(*args, **kwargs)

    class Meta:
        ordering = ['mission', 'time1_in', 'time2_in', 'time3_in']
        verbose_name = 'Sign-in'
