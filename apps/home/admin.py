from django.contrib import admin

# are imported the models of the application
from aRAT.apps.home.models import (Antenna, PAD,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration,
                                   HolographyConfiguration,
                                   TableHeader)
from aRAT.apps.common.models import Configuration

from django.contrib.admin.sites import AdminSite

from django.conf.urls import patterns, url
from django.conf import settings
from django.template.response import TemplateResponse

# is imported the class that provide the checkConsistency
# web service
from aRAT.apps.webServices.checkConsistency.views import (
    checkConsistencyService)


class AntennaAdmin(admin.ModelAdmin):
    """
    Modifier to admin view of Antennas, also this class provide
    a method to update the antennas from the cfg files
    """

    actions = None

    list_display = ('__unicode__', 'current_ste', 'requested_ste')
    list_filter = ['vendor', 'current_ste', 'requested_ste', 'active']
    search_fields = ['name']
    ordering = ['current_ste', 'requested_ste']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': ('*the field active refers to if the Antenna '
                                'can be used for a request (default: active)')
                }),
        ('Request Options', {
                'classes': ('collapse',),
                'fields': ('current_ste',
                           'requested_ste',
                           'current_band',
                           'requested_band',
                           'requester',
                           'request_date'),
                })
        )

    def has_add_permission(self, request):
        "Nobody have permission to add a PAD"
        return False

    def get_urls(self):
        """
        Update the urls to add update_antenna
        """
        urls = patterns('',
                         url(r'^update_antennas/$',
                             self.admin_site.admin_view(
                    self.update_antennas_view),
                             name="update_antennas_view")
                         )
        urls += super(AntennaAdmin, self).get_urls()

        return urls

    def update_antennas_view(self, request):
        """
        view that allows update the antennas in the db from the cfg
        file
        """
        error = ""
        antennas = []
        changes = []

        default_ste = 'VENDOR'

        if error == '':
            file_lines = open(settings.CONFIGURATION_DIR + 'antennas.cfg')
            file_lines = file_lines.readlines()
            for line_string in file_lines:
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
                            changes.append("The vendor of %s was updated."
                                           % antenna)
                        antennas.append(antenna)
                    else:
                        new_antenna = Antenna(name=name_antenna)
                        new_antenna.current_ste = default_ste
                        new_antenna.vendor = vendor
                        new_antenna.save()
                        antennas.append(new_antenna)
                        changes.append("The Antenna %s was added."
                                       % new_antenna)

            for antenna in Antenna.objects.all():
                if antenna not in antennas:
                    changes.append("The Antenna %s was deleted."
                                   % antenna)
                    antenna.delete()

        consistent = checkConsistencyService.check() == "SUCCESS"

        ctx = {'title': 'Update Antennas',
               'changes': changes,
               'error': error,
               'consistent': consistent
               }

        return TemplateResponse(request,
                                "admin/update_configuration.html",
                                ctx)


class PADAdmin(admin.ModelAdmin):
    """
    Class that modify the administration panel view for the antennas
    """
    actions = None

    list_display = ('name', 'location')
    list_display_links = ('name',)
    list_filter = ['location', 'active']
    search_fields = ['name', 'location',
                     'current_antenna__name', 'requested_antenna__name']
    ordering = ['location', 'name']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': ('*the field active refers to if the PAD can '
                                'be used for a request (default: active)')
                }),
        ('Request Options', {
                'classes': ('collapse',),
                'fields': ('current_antenna',
                           'requested_antenna',
                           'requester',
                           'request_date'),
                })
        )

    def has_add_permission(self, request):
        "Nobody have permission to add a PAD"
        return False

    def has_delete_permission(self, request, obj=None):
        "Nobody have permission to delete a PAD"
        return False

    def get_urls(self):
        "Add the update_pads to the urls"
        urls = patterns('',
                         url(r'^update_pads/$',
                             self.admin_site.admin_view(self.update_pads_view),
                             name="update_pads_view")
                         )
        urls += super(PADAdmin, self).get_urls()

        return urls

    def update_pads_view(self, request):
        """
        View that allows update the PAD configurations from
        pads.cfg
        """

        error = ''
        pads = []
        changes = []
        file_lines = open(settings.CONFIGURATION_DIR + 'pads.cfg')
        file_lines = file_lines.readlines()
        for line_string in file_lines:
            line_string = line_string.strip()
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                pad_name, location = line_string.split()
                if PAD.objects.filter(name=pad_name):
                    pad = PAD.objects.get(name=pad_name)
                    if pad.location != location:
                        changes.append("The %s location was updated." % pad)
                        pad.location = location
                        pad.save()
                    pads.append(pad)
                else:
                    new_pad = PAD(name=pad_name)
                    new_pad.location = location
                    new_pad.save()
                    pads.append(new_pad)
                    changes.append("The %s was added." % new_pad)

        for pad in PAD.objects.all():
            if pad not in pads:
                changes.append("The %s was deleted." % pad)
                pad.delete()

        consistent = checkConsistencyService.check() == "SUCCESS"

        ctx = {'title': 'Update PADs',
               'changes': changes,
               'error': error,
               'consistent': consistent
               }

        return TemplateResponse(request,
                                "admin/update_configuration.html",
                                ctx)


class CorrelatorConfigurationAdmin(admin.ModelAdmin):
    """
    Model that allows modify the view in administration panel to
    CorrelatorConfiguration class/model
    """
    actions = None

    list_display = ('caimap', 'configuration', 'correlator')
    list_display_links = ('caimap', 'configuration')
    list_filter = ['correlator', 'active']
    search_fields = ['caimap', 'correlator', 'configuration',
                     'current_antenna__name', 'requested_antenna__name']
    ordering = ['correlator', 'caimap']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': ('*the field active refers to if the '
                                'configuration can be used for a request '
                                '(default: active)')
                }),
        ('Request Options', {
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna',
                           'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        "Nobody have permission to add a new Corr Configuration"
        return False

    def has_delete_permission(self, request, obj=None):
        "Nobody have permission to delete a Corr Configuration"
        return False

    def get_urls(self):
        "The update_configuration is add to the urls of the Model"

        urls = patterns('',
                        url(r'^update_configurations/$',
                            self.admin_site.admin_view(
                    self.update_configurations_view),
                            name="update_configurations_view")
                        )
        urls += super(CorrelatorConfigurationAdmin, self).get_urls()

        return urls

    def update_configurations_view(self, request):
        "View that update the corr configs from corr_configs file"
        error = ''
        changes = []
        corr_confs = []

        header = None
        file_lines = open(settings.CONFIGURATION_DIR + 'corr_configs.cfg')
        file_lines = file_lines.readlines()
        for line_string in file_lines:
            line_string = line_string.strip()
            #the comments are ignored
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                line_list = line_string.split()

                # the - are replaced to spaces
                line_list[0:-1] = [x.replace('-', ' ')
                                   for x in line_list[0:-1]]
                if line_string[0] == "#":
                    line_list[0:-1] = [x.replace('#', '')
                                       for x in line_list[0:-1]]

                    # if the table header exist is added to the object,
                    # if not is created
                    if TableHeader.objects.filter(resource=line_list[-1]):
                        header = TableHeader.objects.get(
                            resource=line_list[-1])
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

                    if CorrelatorConfiguration.objects.filter(
                        caimap=caimap,
                        correlator=correlator):
                        corr_config = CorrelatorConfiguration.objects.get(
                            caimap=caimap,
                            correlator=correlator)

                        if corr_config.configuration != unicode(configuration):
                            corr_config.configuration = unicode(configuration)
                            corr_config.save()
                            changes.append("The %s was updated." % corr_config)
                        corr_confs.append(corr_config)
                    else:
                        new_corr_config = CorrelatorConfiguration(
                            caimap=caimap,
                            correlator=correlator)
                        new_corr_config.configuration = unicode(configuration)
                        new_corr_config.header = header
                        new_corr_config.save()
                        changes.append("The %s was added." % new_corr_config)
                        corr_confs.append(new_corr_config)

        for corr_config in CorrelatorConfiguration.objects.all():
            if corr_config not in corr_confs:
                changes.append("The %s was deleted." % corr_config)
                corr_config.delete()

        consistent = checkConsistencyService.check() == "SUCCESS"

        ctx = {'title': 'Update Correlator Configurations',
               'changes': changes,
               'error': error,
               'consistent': consistent
               }
        return TemplateResponse(request,
                                "admin/update_configuration.html",
                                ctx)


class CentralloConfigurationAdmin(admin.ModelAdmin):
    """
    Modify the administration panel view to CentralloConfiguration
    """

    actions = None

    list_display = ('identifier', 'configuration', 'centrallo')
    list_display_links = ('identifier', 'configuration')
    list_filter = ['centrallo', 'active']
    search_fields = ['identifier', 'centrallo',
                     'current_antenna__name', 'requested_antenna__name']
    ordering = ['centrallo', 'identifier']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': ('*the field active refers to if the '
                                'configuration can be used for a request '
                                '(default: active)')
                }),
        ('Request Options', {
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna',
                           'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        """Nobody have permission to add a new CLO config"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Nobody have permission to delete a CLO config"""
        return False

    def get_urls(self):
        """Add the update_configurations to urls of the model"""
        urls = patterns('',
                        url(r'^update_configurations/$',
                            self.admin_site.admin_view(
                    self.update_configurations_view),
                            name="update_configurations_view")
                        )
        urls += super(CentralloConfigurationAdmin, self).get_urls()

        return urls

    def update_configurations_view(self, request):
        """
        Allows update the CentralLO Configurations from the clo_configs file
        """

        error = ''
        changes = []
        clo_confs = []

        header = None
        file_lines = open(settings.CONFIGURATION_DIR + 'clo_configs.cfg')
        file_lines = file_lines.readlines()

        for line_string in file_lines:
            line_string = line_string.strip()
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                line_list = line_string.split()
                line_list[0:-1] = [x.replace('-', ' ')
                                   for x in line_list[0:-1]]
                if line_string[0] == "#":
                    line_list[0:-1] = [x.replace('#', '')
                                       for x in line_list[0:-1]]

                    # if the table header not exist this is created
                    if TableHeader.objects.filter(
                        resource=line_list[-1]):
                        header = TableHeader.objects.get(
                            resource=line_list[-1])
                        header.text = str(line_list[0:-1])
                        header.save()
                    else:
                        new_header = TableHeader(text=str(line_list[0:-1]),
                                                 resource=line_list[-1])
                        new_header.save()
                else:
                    # is used the element in the first column as identifier
                    identifier = line_list[0]
                    configuration = line_list[1:-1]
                    centrallo = line_list[-1]

                    header = TableHeader.objects.get(resource=centrallo)

                    if CentralloConfiguration.objects.filter(
                        identifier=identifier,
                        centrallo=centrallo):
                        clo_config = CentralloConfiguration.objects.get(
                            identifier=identifier,
                            centrallo=centrallo)

                        if clo_config.configuration != unicode(configuration):
                            clo_config.configuration = unicode(configuration)
                            clo_config.save()
                            changes.append("The %s was updated." % clo_config)
                        clo_confs.append(clo_config)
                    else:
                        new_clo_config = CentralloConfiguration(
                            identifier=identifier,
                            centrallo=centrallo)
                        new_clo_config.configuration = unicode(configuration)
                        new_clo_config.header = header
                        new_clo_config.save()
                        changes.append("The %s was added." % new_clo_config)
                        clo_confs.append(new_clo_config)

        # the configurations that not appears in the cfg file are deleted
        for clo_config in CentralloConfiguration.objects.all():
            if clo_config not in clo_confs:
                changes.append("The %s was deleted." % clo_config)
                clo_config.delete()

        consistent = checkConsistencyService.check() == "SUCCESS"

        ctx = {'title': 'Update CentralLO Configurations',
               'changes': changes,
               'error': error,
               'consistent': consistent
               }

        return TemplateResponse(request,
                                "admin/update_configuration.html",
                                ctx)


class HolographyConfigurationAdmin(admin.ModelAdmin):
    """
    Modify the administration panel view to HolographyConfiguration
    Model
    """

    actions = None

    list_display = ('name',)
    list_display_links = ('name',)
    list_filter = ['active']
    search_fields = ['name', 'current_antenna__name',
                     'requested_antenna__name']

    fieldsets = (
        (None, {
                'fields': ('active',),
                'description': ('*the field active refers to if the PAD can be'
                                ' used for a request (default: active)')
                }),
        ('Request Options', {
                'classes': ('collapse',),
                'fields': ('current_antenna', 'requested_antenna',
                           'requester', 'request_date'),
                })
        )

    def has_add_permission(self, request):
        """Nobody have permissions to add a new HolographyConfiguration"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Nobody have permission to delete an HolographyConfiguration"""
        return False

    def get_urls(self):
        """Add the update_configurations url to the Model's urls"""
        urls = patterns('',
                         url(r'^update_configurations/$',
                             self.admin_site.admin_view(
                    self.update_configurations_view),
                             name="update_configurations_view")
                         )
        urls += super(HolographyConfigurationAdmin, self).get_urls()

        return urls

    def update_configurations_view(self, request):

        error = ''
        holos = []
        changes = []

        file_lines = open(settings.CONFIGURATION_DIR + 'holography.cfg')
        file_lines = file_lines.readlines()
        for line_string in file_lines:
            line_string = line_string.strip()
            is_comment = line_string[0:2] == "//"

            if line_string and not is_comment:
                holo_name = line_string
                if HolographyConfiguration.objects.filter(name=holo_name):
                    holo = HolographyConfiguration.objects.get(name=holo_name)
                    holos.append(holo)
                else:
                    new_holo = HolographyConfiguration(name=holo_name)
                    new_holo.save()
                    holos.append(new_holo)
                    changes.append("The %s was added." % new_holo)

        for holo in HolographyConfiguration.objects.all():
            if holo not in holos:
                changes.append("The %s was deleted." % holo)
                holo.delete()

        consistent = checkConsistencyService.check() == "SUCCESS"

        ctx = {'title': 'Update Holography Receptors',
               'changes': changes,
               'error': error,
               'consistent': consistent
               }

        return TemplateResponse(request,
                                "admin/update_configuration.html",
                                ctx)


class CustomAdminSite(AdminSite):
    """
    Overwrite the default AdminSite class to modify the index view
    """

    def index(self, request, extra_context=None):
        """
        Modify the index view to add controllers for the web services
        (blockUnblock and applyChanges) since the administration panel
        """

        try:
            block_status = Configuration.objects.get(setting='BLOCK')
        except:
            block_status = Configuration(setting='BLOCK', value=False)
            block_status.save()

        requester_group = Group.objects.filter(name='Requester')
        if not requester_group:
            requester_group = Group(name='Requester')
            requester_group.save()

        consistent = checkConsistencyService.check() == "SUCCESS"

        # are passed the read_only status and the consistency status to the
        # template
        extra_context = {'read_only': block_status.value,
                         'consistent': consistent}
        return super(CustomAdminSite, self).index(request,
                                                  extra_context=extra_context)

custom_admin_site = CustomAdminSite()

custom_admin_site.register(Antenna, AntennaAdmin)
custom_admin_site.register(PAD, PADAdmin)
custom_admin_site.register(CorrelatorConfiguration,
                           CorrelatorConfigurationAdmin)
custom_admin_site.register(CentralloConfiguration, CentralloConfigurationAdmin)
custom_admin_site.register(HolographyConfiguration,
                           HolographyConfigurationAdmin)

# Are registered the User and Group models to can modify the
# users (permissions, groups) from the administration panel
from django.contrib.auth.models import User, Group
custom_admin_site.register(User)
custom_admin_site.register(Group)
