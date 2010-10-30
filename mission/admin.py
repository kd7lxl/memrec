from models import *
from django.contrib import admin

class SigninAdmin(admin.ModelAdmin):
    list_display = (
        'mission',
        'person',
        'time_in',
        'time_out',
        'hours',
        'miles_driven',
    )
    list_display_links = (
        'time_in',
        'time_out',
    )
    list_filter = (
        'mission',
        'person',
    )
admin.site.register(Signin, SigninAdmin)

class SigninInline(admin.TabularInline):
    model = Signin

class MissionAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'mission_type',
        'county',
        'total_hours',
        'total_miles',
    )
    list_filter = (
        'mission_type',
        'county',
    )
    readonly_fields = (
        'total_hours',
        'total_miles',
    )
    inlines = (SigninInline,)
    save_on_top = True

admin.site.register(Mission, MissionAdmin)
