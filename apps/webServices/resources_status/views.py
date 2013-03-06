from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc

# are imported the models of the application
from aRAT.apps.home.models import (Antenna, PAD,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration)
from aRAT.apps.webServices.checkConsistency.views import (
    checkConsistencyService)
import json


class ResourcesStatus(ServiceBase):
    """
    Class that expose a method that return the current status
    of the request in JSON format
    """
    @rpc(_returns=String)
    def status_json(ctx):
        """
        Return a String with the current status of the request
        in JSON format
        """

        if checkConsistencyService.check() != 'SUCCESS':
            return ('FAILURE: The current status of the system '
                    'is not consistent.')

        result = {'ste': {}}

        antennas = {}

        for antenna in Antenna.objects.all():
            show_antenna = False

            antenna_data = {'show_antenna': False,
                            'ste': None,
                            'drxbbpr0': None,
                            'drxbbpr1': None,
                            'drxbbpr2': None,
                            'drxbbpr3': None,
                            'dtsrbbpr0': None,
                            'dtsrbbpr1': None,
                            'dtsrbbpr2': None,
                            'dtsrbbpr3': None,
                            'cai': None,
                            'acacai': None,
                            'bands': None,
                            'sas': None,
                            'llc': None,
                            'pad': None
                            }

            ste = antenna.current_ste

            if antenna.is_requested():
                show_antenna = True
                if antenna.is_ste_request():
                    ste = antenna.requested_ste

                    if antenna.current_ste != 'VENDOR':
                        if antenna.current_ste not in result['ste']:
                            result['ste'].setdefault(antenna.current_ste, [])

                        result['ste'][antenna.current_ste].append(
                            {"%s" % antenna: None})

            # is added the bands information
            antenna_data['bands'] = antenna.current_band
            if antenna.is_band_request():
                antenna_data['bands'] = antenna.requested_band

            antenna_data['ste'] = ste
            antenna_data['show_antenna'] = show_antenna

            antennas.setdefault("%s" % antenna, antenna_data)

        # PAD Information
        for pad in PAD.objects.all():
            if pad.is_requested():
                if pad.requested_antenna is not None:
                    antenna = antennas["%s" % pad.requested_antenna]
                    antenna['show_antenna'] = True
                    antenna['pad'] = ("%s" % pad.name)
                elif pad.current_antenna is not None:
                    antennas["%s" % pad.current_antenna]['show_antenna'] = True
            elif pad.current_antenna is not None:
                antennas["%s" % pad.current_antenna]['pad'] = ("%s" % pad.name)

        # Corr Conf Information
        for corr_conf in CorrelatorConfiguration.objects.all():
            if corr_conf.is_requested():
                if corr_conf.requested_antenna is not None:
                    antenna = antennas["%s" % corr_conf.requested_antenna]
                    antenna['show_antenna'] = True
                    if corr_conf.correlator != 'ACA-Corr':
                        (antenna['drxbbpr0'],
                         antenna['drxbbpr1'],
                         antenna['drxbbpr2'],
                         antenna['drxbbpr3']) = corr_conf.drx_data()
                        antenna['cai'] = corr_conf.cai_data()
                    else:
                        (antenna['dtsrbbpr0'],
                         antenna['dtsrbbpr1'],
                         antenna['dtsrbbpr2'],
                         antenna['dtsrbbpr3']) = corr_conf.dtsr_data()
                        antenna['acacai'] = corr_conf.acacai_data()
                elif corr_conf.current_antenna is not None:
                    antenna = antennas["%s" % corr_conf.current_antenna]
                    antenna['show_antenna'] = True
            elif corr_conf.current_antenna is not None:
                antenna = antennas["%s" % corr_conf.current_antenna]
                if corr_conf.correlator != 'ACA-Corr':
                    (antenna['drxbbpr0'],
                     antenna['drxbbpr1'],
                     antenna['drxbbpr2'],
                     antenna['drxbbpr3']) = corr_conf.drx_data()
                    antenna['cai'] = corr_conf.cai_data()
                else:
                    (antenna['dtsrbbpr0'],
                     antenna['dtsrbbpr1'],
                     antenna['dtsrbbpr2'],
                     antenna['dtsrbbpr3']) = corr_conf.dtsr_data()
                    antenna['acacai'] = corr_conf.acacai_data()

        # CentralLO information
        for clo_conf in CentralloConfiguration.objects.all():
            if clo_conf.is_requested():
                if clo_conf.requested_antenna is not None:
                    antenna = antennas["%s" % clo_conf.requested_antenna]
                    antenna['show_antenna'] = True

                    antenna['sas'] = "%s-%s" % (
                        clo_conf.sas_ch(), clo_conf.sas_node())
                    antenna['llc'] = "%s-%s" % (
                        clo_conf.llc_ch(), clo_conf.llc_node())
                elif clo_conf.current_antenna is not None:
                    antenna = antennas["%s" % clo_conf.current_antenna]
                    antenna['show_antenna'] = True
            elif clo_conf.current_antenna is not None:
                antenna = antennas["%s" % clo_conf.current_antenna]

                antenna['sas'] = "%s-%s" % (
                    clo_conf.sas_ch(), clo_conf.sas_node())
                antenna['llc'] = "%s-%s" % (
                    clo_conf.llc_ch(), clo_conf.llc_node())

        # -----------------------------------
        # Holography Receptor Information
        #
        #          Not included
        #
        # -----------------------------------

        for antenna_name, antenna_data in antennas.iteritems():
            if antenna_data['ste'] == 'VENDOR':
                continue

            if antenna_data['show_antenna']:
                ste = antenna_data['ste']
                if ste not in result['ste']:
                    result['ste'].setdefault(ste, [])

                del antenna_data['show_antenna']
                del antenna_data['ste']

                result['ste'][ste].append({"%s" % antenna_name: antenna_data})

        if result['ste'] != {}:
            return json.dumps(result)
        else:
            return 'DOES NOT EXIST CHANGES.'

resources_status_service = csrf_exempt(
    DjangoApplication(Application([ResourcesStatus],
                                  'cl.alma.arat.webservice.ResourcesStatus',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
