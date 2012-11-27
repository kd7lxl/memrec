from models import *
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from datetime import date


class NullFilterSpec(SimpleListFilter):
    title = u''
    parameter_name = u''

    def lookups(self, request, model_admin):
        return (
            ('1', self.title),
            ('0', 'Not %s' % self.title),
        )

    def queryset(self, request, queryset):
        kwargs = {
            str('%s__isnull' % self.parameter_name): True,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class DroppedNullFilterSpec(NullFilterSpec):
    title = u'Dropped'
    parameter_name = u'drop_date'


class AdultFilterSpec(SimpleListFilter):
    title = u'Age'
    parameter_name = u'dob'

    def lookups(self, request, model_admin):
        return (
            ('youth', 'Youth'),
            ('adult', 'Adult'),
        )

    def queryset(self, request, queryset):
        today = date.today()
        twenty_one = today.replace(year=(today.year - 21))
        if self.value() == 'youth':
            return queryset.filter(dob__gt=twenty_one)
        if self.value() == 'adult':
            return queryset.filter(dob__lte=twenty_one)
        return queryset


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'dem_number',
        'join_date',
        'years_in_unit',
        'is_adult',
    )
    list_filter = (
        'join_date',
        DroppedNullFilterSpec,
        AdultFilterSpec,
    )
    search_fields = (
        'last_name',
        'first_name',
        'dem_number',
    )
    save_on_top = True
admin.site.register(Person, PersonAdmin)

admin.site.register(MembershipFeePayment)


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sms_email_hostname',
    )
admin.site.register(ServiceProvider, ServiceProviderAdmin)
