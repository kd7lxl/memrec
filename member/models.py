from django.db import models
from django.core.validators import RegexValidator

from datetime import date
import re

phone_re = re.compile(r'^[\d]{10}$')
validate_phone = RegexValidator(phone_re, (u"Enter a 10-digit phone number with no punctuation."), 'invalid')

hostname_re = re.compile(r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$')
validate_hostname = RegexValidator(hostname_re, (u"Enter a valid hostname."), 'invalid')


class Person(models.Model):
    """
    Create a person:
    >>> person = Person(last_name='Smith', first_name='John')
    >>> person.save()
    >>> person
    <Person: John Smith>
    """
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    dem_number = models.PositiveIntegerField(null=True, blank=True)
    dob = models.DateField(null=True,blank=True)
    join_date = models.DateField(null=True, blank=True)
    person_type = models.CharField(max_length=20, choices=(
        ('contact', 'contact'),
        ('recruit', 'recruit'),
        ('member', 'member'),
    ))
    emergency_contact_1 = models.ForeignKey('self', blank=True, null=True, related_name='emergency_contact1_for')
    emergency_contact_2 = models.ForeignKey('self', blank=True, null=True, related_name='emergency_contact2_for')
    date_added = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    
    def age(self, today=date.today()):
        born = self.dob
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except:
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            yearsold = today.year - born.year - 1
        else:
            yearsold = today.year - born.year
        if yearsold == 0:
            if birthday > today:
                monthsold = today.month - born.month - 1
            else:
                monthsold = today.month - born.month
            return '%s mo' % (monthsold)
        elif yearsold == 1:
            return '%s yr' % (yearsold)
        else:
            return '%s yrs' % (yearsold)
    
    def time_in_unit(self, today=date.today()):
        born = self.join_date
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except:
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            yearsold = today.year - born.year - 1
        else:
            yearsold = today.year - born.year
        if yearsold == 0:
            if birthday > today:
                monthsold = today.month - born.month - 1
            else:
                monthsold = today.month - born.month
            return '%s mo' % (monthsold)
        elif yearsold == 1:
            return '%s yr' % (yearsold)
        else:
            return '%s yrs' % (yearsold)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
class MembershipFeePayment(models.Model):
    person = models.ForeignKey(Person)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return u'%s paid $%02.f on %s' % (self.person, self.payment_amount, self.payment_date)

class EmailAddress(models.Model):
    person = models.ForeignKey(Person)
    email_address = models.EmailField()
    
    def __unicode__(self):
        return u'%s' % (self.email_address)
    
    class Meta:
        verbose_name_plural = 'email addresses'

class Address(models.Model):
    person = models.ForeignKey(Person)
    address1 = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=9)
    
    class Meta:
        verbose_name_plural = 'addresses'

class ServiceProvider(models.Model):
    name = models.CharField(max_length=30)
    sms_email_hostname = models.CharField(max_length=60, validators=[validate_hostname])
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    class Meta:
        ordering = ['name']

class Phone(models.Model):
    person = models.ForeignKey(Person)
    phone_number = models.CharField(max_length=10, validators=[validate_phone], help_text='Numbers only please, no punctuation.')
    phone_type = models.CharField(max_length=10, null=True, blank=True, choices=(
        ('home', 'home'),
        ('work', 'work'),
        ('mobile', 'mobile'),
        ('pager', 'pager'),
        ('fax', 'fax'),
    ))
    service_provider = models.ForeignKey(ServiceProvider, null=True, blank=True)
    sms_enabled = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'(%s) %s-%s' % (
            self.phone_number[0:3],
            self.phone_number[3:6],
            self.phone_number[6:10],
        )
    
    def sms_email_address(self):
        if self.service_provider is not None \
        and self.sms_enabled is True:
            return '%s@%s' % (self.phone_number, self.service_provider.sms_email_hostname)
    
    class Meta:
        verbose_name = 'phone number'
