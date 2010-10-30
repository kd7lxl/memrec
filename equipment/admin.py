from models import *
from django.contrib import admin

class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'equipment_type',
        'manufacturer',
        'model',
        'serial',
        'label',
        'value',
    )
    list_filter = (
        'equipment_type',
        'manufacturer',
        'model',
    )
admin.site.register(Equipment, EquipmentAdmin)

class EquipmentCheckoutAdmin(admin.ModelAdmin):
    list_display = (
        'equipment',
        'person',
        'date_out',
        'date_in',
    )
    list_filter = (
        'date_out',
        'date_in',
    )
    search_fields = (
        'person__last_name',
        'person__first_name',
        'equipment__equipment_type',
        'equipment__manufacturer',
        'equipment__model',
        'equipment__serial',
        'equipment__label',
        'date_out',
        'date_in',
    )
admin.site.register(EquipmentCheckout, EquipmentCheckoutAdmin)