from models import *
from django.contrib import admin

class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0

class PersonAdmin(admin.ModelAdmin):
    inlines = [
        EmailAddressInline,
        AddressInline,
        PhoneInline,
    ]
    list_display = (
        '__unicode__',
        'dem_number',
        'person_type',
        'join_date',
        'age',
        'time_in_unit',
    )
    list_filter = (
        'person_type',
        'join_date',
    )
    search_fields = (
        'last_name',
        'first_name',
        'dem_number',
    )
    save_on_top = True
admin.site.register(Person, PersonAdmin)

class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        'person',
        '__unicode__',
        'phone_type',
        'service_provider',
        'sms_enabled',
        'sms_email_address',
    )
    list_filter = (
        'phone_type',
        'service_provider',
        'sms_enabled',
    )
    search_fields = (
        'person__last_name',
        'person__first_name',
        'phone_number',
    )
admin.site.register(Phone, PhoneAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'person',
        'address1',
        'address2',
        'city',
        'state',
        'postal_code',
    )
    list_filter = (
        'postal_code',
        'city',
        'state',
    )
    search_fields = (
        'person__last_name',
        'person__first_name',
        'address1',
        'address2',
        'city',
        'state',
        'postal_code',
    )
admin.site.register(Address, AddressAdmin)

admin.site.register(MembershipFeePayment)

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sms_email_hostname',
    )
admin.site.register(ServiceProvider, ServiceProviderAdmin)
