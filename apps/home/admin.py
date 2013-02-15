from aRAT.apps.webServices.blockUnblock.views import blockUnblockService

from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration
from aRAT.apps.common.models import Configuration

from django.contrib.admin.sites import AdminSite

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


from aRAT.apps.webServices.checkConsistency.views import checkConsistencyService

class CustomAdminSite(AdminSite):

    def index(self, request, extra_context=None):
        block_status = Configuration.objects.get(setting='BLOCK')

        consistent = checkConsistencyService.check("") == "SUCCESS"

        extra_context = {'read_only': block_status.value,
                         'consistent': consistent}
        return super(CustomAdminSite, self).index(request, extra_context=extra_context)

custom_admin_site = CustomAdminSite()

custom_admin_site.register(Antenna, AntennaAdmin)
custom_admin_site.register(PAD, PADAdmin)
custom_admin_site.register(CorrelatorConfiguration, CorrelatorConfigurationAdmin)
custom_admin_site.register(CentralloConfiguration, CentralloConfigurationAdmin)
custom_admin_site.register(HolographyConfiguration, HolographyConfigurationAdmin)

from django.contrib.auth.models import User, Group
custom_admin_site.register(User)
custom_admin_site.register(Group)

#admin_urls = get_admin_urls()
#admin.site.get_urls = admin_urls
