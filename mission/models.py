from django.db import models
from member.models import Person

MISSION_TYPE = (
    ('mission', 'Mission'),
    ('training', 'Training'),
)


class Mission(models.Model):
    mission_number = models.CharField(max_length=10, unique=True)
    mission_type = models.CharField(max_length=10, choices=MISSION_TYPE)
    mission_name = models.CharField(max_length=30, null=True, blank=True)
    county = models.CharField(max_length=30)
    date_start = models.DateField()
    date_end = models.DateField()
    signed_in = models.ManyToManyField(Person, through='Signin')

    def __unicode__(self):
        if self.mission_name:
            return u'%s (%s)' % (self.mission_number, self.mission_name)
        return self.mission_number

    def total_hours(self):
        return sum([signin.hours() for signin in self.signin_set.all()])

    def total_miles(self):
        return sum([signin.miles_driven for signin in self.signin_set.all()])


class Signin(models.Model):
    mission = models.ForeignKey(Mission)
    person = models.ForeignKey(Person)
    assignment = models.CharField(max_length=16, null=True, blank=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    miles_driven = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s @ %s' % (self.person, self.mission)

    def hours(self):
        duration = self.time_out - self.time_in
        return int(duration.days * 24 + duration.seconds / 3600) + 1

    class Meta:
        verbose_name = 'Sign-in'
