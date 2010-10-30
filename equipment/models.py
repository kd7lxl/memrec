from django.db import models
from member.models import Person

class Equipment(models.Model):
    equipment_type = models.CharField(max_length=30, null=True, blank=True, help_text='e.g., Radio, GPS, Vehicle')
    manufacturer = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    value = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, help_text='Enter the value in dollars (no dollar sign).')
    label = models.CharField(max_length=30, null=True, blank=True, help_text='i.e., engraving')
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.model, self.label)
    
    class Meta:
        verbose_name_plural = 'equipment'

class EquipmentCheckout(models.Model):
    equipment = models.ForeignKey(Equipment)
    person = models.ForeignKey(Person)
    date_out = models.DateField()
    date_in = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s to %s' % (self.equipment, self.person)
    
    class Meta:
        ordering = ('-date_out',)
