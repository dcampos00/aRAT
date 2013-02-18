from aRAT.apps.webServices.blockUnblock.views import blockUnblockService

from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration, TableHeader
from aRAT.apps.common.models import Configuration

from django.contrib.admin.sites import AdminSite

from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.conf import settings
from django.shortcuts import render_to_response

from django.template.response import TemplateResponse

class AntennaAdmin(admin.ModelAdmin):
    actions = None

    list_display = ('__unicode__', 'current_ste', 'requested_ste')
    list_filter = ['vendor', 'current_ste', 'requested_ste', 'active']
    search_fields = ['name']
    ordering = ['current_ste', 'requested_ste']

    def get_urls(self):
        urls = patterns('',
                         url(r'^update_antennas/$', self.admin_site.admin_view(self.update_antennas_view), name="update_antennas_view")
                         )
        urls += super(AntennaAdmin, self).get_urls()

        return urls

    def update_antennas_view(self, request):
        error = ""
        antennas = []
        changes = []

        STEs = tuple([tuple([ln, i.strip()]) 
                      for ln, i 
                      in enumerate(open(settings.CONFIGURATION_DIR+'stes.cfg')) 
                      if i.strip()])

        for ste in STEs:
            if 'VENDOR' in ste:
                default_ste = ste[0]
                error = ''
                break
            else:
                error = 'The STE VENDOR does not exist!'

        if error == '':
            for line_string in open(settings.CONFIGURATION_DIR+'antennas.cfg').readlines():
                line_string.strip()
                is_comment = line_string[0:2] == "//"

                if line_string and not is_comment:
                    name_antenna, vendor = line_string.split()
                    vendor = vendor.replace('-', ' ')
                    
                    if Antenna.objects.filter(name=name_antenna):
                        antenna = Antenna.objects.get(name=name_antenna)
                        if antenna.vendor != vendor:
                            antenna.vendor = vendor
                            antenna.save()
                            changes.append("The vendor of %s was updated."%antenna)
                        antennas.append(antenna)
                    else:                            
                        new_antenna = Antenna(name=name_antenna)
                        new_antenna.current_ste = default_ste
                        new_antenna.vendor = vendor
                        new_antenna.save()
                        antennas.append(new_antenna)
                        changes.append("The Antenna %s was added."%new_antenna)

            for antenna in Antenna.objects.all():
                if antenna not in antennas:
                    changes.append("The Antenna %s was deleted."%antenna)
                    antenna.delete()

        ctx = {'title': 'Update Antennas',
               'changes': changes,
               'error': error,
               }

        return TemplateResponse(request, "admin/update_configuration.html", ctx);

class PADAdmin(admin.ModelAdmin):
    actions = None

    #list_display = ('line_number', 'name', 'location')
    list_display = ('name', 'location')
    list_display_links = ('name',)
    list_filter = ['location', 'active']
    search_fields = ['name', 'location', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['location', 'name']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': '*the field active refers to if the PAD can be used for a request (default: active)'
                }),
        ('Request Options',{
                'classes': ('collapse',),
                'fields': ('current_antenna',
                           'requested_antenna',
                           'requester',
                           'request_date'),
                })
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = patterns('',
                         url(r'^update_pads/$',
                             self.admin_site.admin_view(self.update_pads_view),
                             name="update_pads_view")
                         )
        urls += super(PADAdmin, self).get_urls()

        return urls

    def update_pads_view(self, request):

        error = ''
        pads = []
        changes = []

        for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'pads.cfg')):
            line_string = line_string.strip()
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                pad_name, location = line_string.split()
                if PAD.objects.filter(name=pad_name):
                    pad = PAD.objects.get(name=pad_name)
                    if pad.location != location:
                        changes.append("The %s location was updated."%pad)
                        pad.location = location
                        pad.save()
                    pads.append(pad)
                else:
                    new_pad = PAD(name=pad_name)
                    new_pad.location = location
                    new_pad.save()
                    pads.append(new_pad)
                    changes.append("The %s was added."%new_pad)

        for pad in PAD.objects.all():
            if pad not in pads:
                changes.append("The %s was deleted."%pad)
                pad.delete()

        ctx = {'title': 'Update PADs',
               'changes': changes,
               'error': error,
               }

        return TemplateResponse(request, "admin/update_configuration.html", ctx);

class CorrelatorConfigurationAdmin(admin.ModelAdmin):
    actions = None

#    list_display = ('line_number', 'caimap', 'configuration', 'correlator')
    list_display = ('caimap', 'configuration', 'correlator')
    list_display_links = ('caimap', 'configuration')
    list_filter = ['correlator', 'active']
    search_fields = ['line', 'correlator', 'current_antenna__name', 'requested_antenna__name']
    ordering = ['correlator', 'caimap']

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

    def get_urls(self):
        urls = patterns('',
                        url(r'^update_configurations/$',
                            self.admin_site.admin_view(self.update_configurations_view),
                            name="update_configurations_view")
                        )
        urls += super(CorrelatorConfigurationAdmin, self).get_urls()

        return urls

    def update_configurations_view(self, request):
        error = ''
        changes = []
        corr_confs = []
        
        header = None
        
        for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
            line_string = line_string.strip()
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                line_list = line_string.split()
                line_list[0:-1] = [x.replace('-', ' ') for x in line_list[0:-1]]
                if line_string[0] == "#":
                    line_list[0:-1] = [x.replace('#', '') for x in line_list[0:-1]]
                    if TableHeader.objects.filter(resource=line_list[-1]):
                        header = TableHeader.objects.get(resource=line_list[-1])
                        header.text = str(line_list[0:-1])
                        header.save()
                    else:
                        new_header = TableHeader(text=str(line_list[0:-1]),
                                                 resource=line_list[-1])
                        new_header.save()
                else:
                    caimap = line_list[0]
                    configuration = line_list[1:-1]
                    correlator = line_list[-1]

                    header = TableHeader.objects.get(resource=correlator)

                    if CorrelatorConfiguration.objects.filter(caimap=caimap,
                                                              correlator=correlator):
                        corr_config = CorrelatorConfiguration.objects.get(caimap=caimap,
                                                                          correlator=correlator)
                       
                        if corr_config.configuration != unicode(configuration):
                            corr_config.configuration = unicode(configuration)
                            corr_config.save()
                            changes.append("The %s was updated."%corr_config)
                        corr_confs.append(corr_config)
                    else:
                        new_corr_config = CorrelatorConfiguration(caimap=caimap,
                                                                  correlator=correlator)
                        new_corr_config.configuration = unicode(configuration)
                        new_corr_config.header = header
                        new_corr_config.save()
                        changes.append("The %s was added."%new_corr_config)
                        corr_confs.append(new_corr_config)

        for corr_config in CorrelatorConfiguration.objects.all():
            if corr_config not in corr_confs:
                changes.append("The %s was deleted."%corr_config)
                corr_config.delete()
        
        ctx = {'title': 'Update Correlator Configurations',
               'changes': changes,
               'error': error,
               }
        return TemplateResponse(request, "admin/update_configuration.html", ctx);

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
        try:
            block_status = Configuration.objects.get(setting='BLOCK')
        except:
            block_status = Configuration(setting='BLOCK', value=False)
            block_status.save()

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
