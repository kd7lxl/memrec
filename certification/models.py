from django.db import models
from member.models import Person

from datetime import date

CERTIFICATION_TYPE = (
    ('NIMS', 'NIMS'),
    ('SARVAR', 'SARVAC'),
    ('WESAR', 'WESAR'),
)

class Certification(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    years_valid = models.PositiveIntegerField(null=True, blank=True, help_text='How many years is this certifcation valid before expiration? (optional)')
    certification_type = models.CharField('type', max_length=16, choices=CERTIFICATION_TYPE, blank=True)
    prereqs = models.ManyToManyField('self', null=True, blank=True, related_name='prereq_to')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class CertificationEarned(models.Model):
    certification = models.ForeignKey(Certification)
    person = models.ForeignKey(Person)
    date_earned = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.person, self.certification)
    
    def expiration_date(self):
        if not self.certification.years_valid:
            return None
        year, month, day = self.date_earned.timetuple()[:3]
        return date(year + self.certification.years_valid, month, day)
    
    def expired(self):
        expiration_date = self.expiration_date()
        if self.expiration_date() is None:
            return False
        elif date.today() > self.expiration_date():
            return True
        return False
    
    class Meta:
        verbose_name_plural = 'certifications earned'