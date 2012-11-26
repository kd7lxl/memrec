from django.db import models
from django.core.validators import RegexValidator

from datetime import date
import re

phone_re = re.compile(r'^[\d]{10}$')
validate_phone = RegexValidator(phone_re, (u"Enter a 10-digit phone number with no punctuation."), 'invalid')

hostname_re = re.compile(r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$')
validate_hostname = RegexValidator(hostname_re, (u"Enter a valid hostname."), 'invalid')


class Person(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    last_name = models.CharField(max_length=150, db_column='Last Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    first_name = models.CharField(max_length=150, db_column='First name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    middle_initial = models.CharField(max_length=12, db_column='Middle Initial', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    dem_number = models.CharField(max_length=45, db_column='DEM Number', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address = models.CharField(max_length=150, db_column='Address', blank=True) # Field name made lowercase.
    address_2 = models.CharField(max_length=150, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    city = models.CharField(max_length=150, db_column='City', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=150, db_column='State', blank=True) # Field name made lowercase.
    zip = models.CharField(max_length=150, db_column='Zip', blank=True) # Field name made lowercase.
    nextel = models.CharField(max_length=45, db_column='Nextel', blank=True) # Field name made lowercase.
    home_phone = models.CharField(max_length=150, db_column='Home Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    cell_phone = models.CharField(max_length=150, db_column='Cell Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    cell_provider = models.CharField(max_length=120, db_column='Cell Provider', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    text_ok = models.CharField(max_length=3, db_column='Text OK', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    pager = models.CharField(max_length=150, db_column='Pager', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=240, db_column='Email', blank=True) # Field name made lowercase.
    rank = models.CharField(max_length=45, db_column='Rank', blank=True) # Field name made lowercase.
    dob = models.DateField(null=True, db_column='DOB', blank=True) # Field name made lowercase.
    join_date = models.DateField(null=True, db_column='Join Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    drop_date = models.DateField(null=True, db_column='Drop Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    radio_number = models.CharField(max_length=12, db_column='Radio Number', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    ham_callsign = models.CharField(max_length=150, db_column='Ham Callsign', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_pri_name = models.CharField(max_length=150, db_column='Emrg Pri Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_pri_phone = models.CharField(max_length=60, db_column='Emrg Pri Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_pri_alt_phone = models.CharField(max_length=60, db_column='Emrg Pri Alt Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_pri_rel = models.CharField(max_length=60, db_column='Emrg Pri Rel', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_sec_name = models.CharField(max_length=150, db_column='Emrg Sec Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_sec_phone = models.CharField(max_length=60, db_column='Emrg Sec Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_sec_alt_phone = models.CharField(max_length=60, db_column='Emrg Sec Alt Phone', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    emrg_sec_rel = models.CharField(max_length=60, db_column='Emrg Sec Rel', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_reup = models.DateField(null=True, db_column='Last Reup', blank=True) # Field renamed to remove spaces. Field name made lowercase.

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def age(self, today=date.today()):
        born = self.dob
        try:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except:
            birthday = born.replace(year=today.year, day=born.day - 1)
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
        try:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except:
            birthday = born.replace(year=today.year, day=(born.day - 1))
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
        db_table = u'Members'
        ordering = ['last_name', 'first_name']


class MembershipFeePayment(models.Model):
    person = models.ForeignKey(Person)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return u'%s paid $%02.f on %s' % (self.person, self.payment_amount, self.payment_date)

class ServiceProvider(models.Model):
    name = models.CharField(max_length=30)
    sms_email_hostname = models.CharField(max_length=60, validators=[validate_hostname])

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ['name']
