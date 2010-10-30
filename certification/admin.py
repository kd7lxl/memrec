from models import *
from django.contrib import admin

class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'certification_type',
        'years_valid',
    )
    list_filter = (
        'certification_type',
    )
    filter_horizontal = (
        'prereqs',
    )
admin.site.register(Certification, CertificationAdmin)

class CertificationEarnedAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'person',
        'certification',
        'date_earned',
        'expiration_date',
        'expired',
    )
    list_filter = (
        'person',
        'certification',
    )
    search_fields = (
        'person__last_name',
        'person__first_name',
        'certification__name',
    )
admin.site.register(CertificationEarned, CertificationEarnedAdmin)
