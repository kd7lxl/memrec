from models import *
from django.contrib import admin

class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 1

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = [
        EmailAddressInline,
        AddressInline,
        PhoneInline,
    ]
    list_display = (
        '__unicode__',
        'dem_number',
    )
    search_fields = (
        'last_name',
        'first_name',
        'dem_number',
    )
admin.site.register(Person, PersonAdmin)

admin.site.register(Phone)

admin.site.register(MembershipFeePayment)

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sms_email_hostname',
    )
admin.site.register(ServiceProvider, ServiceProviderAdmin)
