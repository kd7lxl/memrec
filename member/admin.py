from models import *
from django.contrib import admin


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
