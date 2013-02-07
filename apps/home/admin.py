from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralLO

class AntennaAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'current_ste')
    list_filter = ['current_ste', 'active']
    search_fields = ['name']

class CorrelatorConfigurationAdmin(admin.ModelAdmin):
    list_display = ('caimap', 'line_number', 'configuration', 'correlator')
    list_display_links = ('caimap', 'line_number', 'configuration')
    list_filter = ['correlator', 'active']
    search_fields = ['line', 'correlator', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['line']

admin.site.register(Antenna, AntennaAdmin)
admin.site.register(PAD)
admin.site.register(CorrelatorConfiguration, CorrelatorConfigurationAdmin)
admin.site.register(CentralLO)
