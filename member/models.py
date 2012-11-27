from django.db import models
from django.core.validators import RegexValidator

from datetime import date
import re

phone_re = re.compile(r'^[\d]{10}$')
validate_phone = RegexValidator(phone_re, (u"Enter a 10-digit phone number with no punctuation."), 'invalid')

hostname_re = re.compile(r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$')
validate_hostname = RegexValidator(hostname_re, (u"Enter a valid hostname."), 'invalid')


def age(born, today=date.today()):
    try:
        return (today - born).days / 365.
    except TypeError:
        return None


class Person(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    last_name = models.CharField(max_length=150, db_column='Last Name', blank=True)
    first_name = models.CharField(max_length=150, db_column='First name', blank=True)
    middle_initial = models.CharField(max_length=12, db_column='Middle Initial', blank=True, null=True)
    dem_number = models.CharField(max_length=45, db_column='DEM Number',
        blank=True, null=True, verbose_name='DEM number')
    address = models.CharField(max_length=150, db_column='Address', blank=True)
    address_2 = models.CharField(max_length=150, db_column='Address 2', blank=True, null=True)
    city = models.CharField(max_length=150, db_column='City', blank=True)
    state = models.CharField(max_length=150, db_column='State', blank=True)
    zip = models.CharField(max_length=150, db_column='Zip', blank=True, null=True)
    nextel = models.CharField(max_length=45, db_column='Nextel', blank=True, null=True)
    home_phone = models.CharField(max_length=150, db_column='Home Phone', blank=True, null=True)
    cell_phone = models.CharField(max_length=150, db_column='Cell Phone', blank=True, null=True)
    cell_provider = models.CharField(max_length=120, db_column='Cell Provider', blank=True, null=True)
    text_ok = models.CharField(max_length=3, db_column='Text OK', blank=True, null=True)
    pager = models.CharField(max_length=150, db_column='Pager', blank=True, null=True)
    email = models.CharField(max_length=240, db_column='Email', blank=True, null=True)
    rank = models.CharField(max_length=45, db_column='Rank', blank=True, null=True)
    dob = models.DateField(null=True, db_column='DOB', blank=True)
    join_date = models.DateField(null=True, db_column='Join Date', blank=True)
    drop_date = models.DateField(null=True, db_column='Drop Date', blank=True)
    radio_number = models.CharField(max_length=12, db_column='Radio Number', blank=True, null=True)
    ham_callsign = models.CharField(max_length=150, db_column='Ham Callsign', blank=True, null=True)
    emrg_pri_name = models.CharField(max_length=150, db_column='Emrg Pri Name',
        blank=True, null=True, verbose_name='Priority Emergency Contact Name')
    emrg_pri_phone = models.CharField(max_length=60, db_column='Emrg Pri Phone',
        blank=True, null=True, verbose_name='Priority Emergency Contact Phone')
    emrg_pri_alt_phone = models.CharField(max_length=60, db_column='Emrg Pri Alt Phone',
        blank=True, null=True, verbose_name='Priority Emergency Contact Alternate Phone')
    emrg_pri_rel = models.CharField(max_length=60, db_column='Emrg Pri Rel',
        blank=True, null=True, verbose_name='Priority Emergency Contact Relation')
    emrg_sec_name = models.CharField(max_length=150, db_column='Emrg Sec Name',
        blank=True, null=True, verbose_name='Secondary Emergency Contact Name')
    emrg_sec_phone = models.CharField(max_length=60, db_column='Emrg Sec Phone',
        blank=True, null=True, verbose_name='Secondary Emergency Contact Phone')
    emrg_sec_alt_phone = models.CharField(max_length=60, db_column='Emrg Sec Alt Phone',
        blank=True, null=True, verbose_name='Secondary Emergency Contact Alternate Phone')
    emrg_sec_rel = models.CharField(max_length=60, db_column='Emrg Sec Rel',
        blank=True, null=True, verbose_name='Secondary Emergency Contact Relation')
    last_reup = models.DateField(null=True, db_column='Last Reup', blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def age(self, today=date.today()):
        try:
            return u'%d' % age(self.dob, today)
        except TypeError:
            return None

    def is_adult(self):
        return self.age() >= 21
    is_adult.admin_order_field = 'dob'
    is_adult.boolean = True

    def years_in_unit(self, today=date.today()):
        try:
            return u'%.1f' % age(self.join_date, today)
        except TypeError:
            return None
    years_in_unit.admin_order_field = 'join_date'

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
