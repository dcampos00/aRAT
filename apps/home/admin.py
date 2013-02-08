from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration

#admin.site.disable_action('delete_selected')

class AntennaAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('__unicode__', 'current_ste', 'requested_ste')
    list_filter = ['current_ste', 'requested_ste', 'active']
    search_fields = ['name']
    ordering = ['current_ste', 'requested_ste']

class PADAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('line_number', 'name', 'location')
    list_display_links = ('name',)
    list_filter = ['location', 'active']
    search_fields = ['line', 'location', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['location', 'line']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': '*the field active refers to if the PAD can be used for a request (default: active)'
                }),
        ('Request Options',{
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna', 'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CorrelatorConfigurationAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('line_number', 'caimap', 'configuration', 'correlator')
    list_display_links = ('caimap', 'line_number', 'configuration')
    list_filter = ['correlator', 'active']
    search_fields = ['line', 'correlator', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['line', 'correlator']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': '*the field active refers to if the configuration can be used for a request (default: active)'
                }),
        ('Request Options',{
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna', 'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CentralloConfigurationAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('line_number', 'configuration', 'centrallo')
    list_display_links = ('line_number', 'configuration')
    list_filter = ['centrallo', 'active']
    search_fields = ['line', 'centrallo', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['line', 'centrallo']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': '*the field active refers to if the configuration can be used for a request (default: active)'
                }),
        ('Request Options',{
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna', 'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class HolographyConfigurationAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('line_number', 'name')
    list_display_links = ('name',)
    list_filter = ['active']
    search_fields = ['line', 'current_antenna__name', 'requested_antenna__name']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': '*the field active refers to if the PAD can be used for a request (default: active)'
                }),
        ('Request Options',{
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna', 'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Antenna, AntennaAdmin)
admin.site.register(PAD, PADAdmin)
admin.site.register(CorrelatorConfiguration, CorrelatorConfigurationAdmin)
admin.site.register(CentralloConfiguration, CentralloConfigurationAdmin)
admin.site.register(HolographyConfiguration, HolographyConfigurationAdmin)
