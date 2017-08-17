from models import *
from widgets import TimeInput
from django.contrib import admin


class SigninAdmin(admin.ModelAdmin):
    list_display = (
        'mission',
        'person',
        'time1_in',
        'hours',
        'miles_driven',
    )
    list_display_links = (
        'time1_in',
    )
    list_filter = (
        'mission',
        'person',
    )
    search_fields = [
        'mission__mission_number',
        'person__first_name',
        'person__last_name',
    ]
admin.site.register(Signin, SigninAdmin)


class SigninInline(admin.TabularInline):
    model = Signin
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput},
    }


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
        'prepared_by',
    )
    inlines = (SigninInline,)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        if obj.prepared_by is None:
            obj.prepared_by = request.user
        obj.save()
admin.site.register(Mission, MissionAdmin)


class MissionCategoryAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'is_mission',
        'is_training',
    )
admin.site.register(MissionCategory, MissionCategoryAdmin)
