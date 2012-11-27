from models import *
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter


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


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'dem_number',
        'join_date',
        'age',
        'years_in_unit',
    )
    list_filter = (
        'join_date',
        DroppedNullFilterSpec,
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
