from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration

import json

class ResourcesStatus(ServiceBase):
    """
    """
    @rpc(_returns=String)
    def status_json(ctx):
        """
        """

        result = {'ste': {}}

        for antenna in Antenna.objects.all():
            deleted = False
            if antenna.is_ste_request():
                ste = antenna.requested_ste
                deleted = True
            else:
                ste = antenna.current_ste

            if ste == 'VENDOR':
                continue

            if ste not in result['ste']:
                result['ste'].setdefault(ste, [])

            antenna_data = {'drxbbpr0': None,
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

            # Correlator Data
            corr_confs = CorrelatorConfiguration.objects.filter(Q(current_antenna=antenna, assigned=True) | Q(requested_antenna=antenna))
            for corr_conf in corr_confs:
                antenna_data['drxbbpr0'], antenna_data['drxbbpr1'], antenna_data['drxbbpr2'], antenna_data['drxbbpr3'] = corr_conf.drx_data()
                antenna_data['dtsrbbpr0'], antenna_data['dtsrbbpr1'], antenna_data['dtsrbbpr2'], antenna_data['dtsrbbpr3'] = corr_conf.dtsr_data()
                antenna_data['cai'], antenna_data['acacai'] = corr_conf.cai_acacai_data()

            # CentralLO Data
            clo_confs = CentralloConfiguration.objects.filter(Q(current_antenna=antenna, assigned=True) | Q(requested_antenna=antenna))
            for clo_conf in clo_confs:
                antenna_data['sas'] = "%s-%s"%(clo_conf.sas_ch(), clo_conf.sas_node())
                antenna_data['llc'] = "%s-%s"%(clo_conf.llc_ch(), clo_conf.llc_node())
            
            # PAD Data
            pads = PAD.objects.filter(Q(current_antenna=antenna, assigned=True) | Q(requested_antenna=antenna))
            for pad in pads:
                antenna_data['pad'] = "%s"%pad.name

            # bands Data
            if antenna.is_band_request():
                bands = antenna.requested_band
            else:
                bands = antenna.current_band

            antenna_data['bands'] = bands

            result['ste'][ste].append({"%s"%antenna: antenna_data})
            
            if deleted and antenna.current_ste != 'VENDOR':
                result['ste'][antenna.current_ste].append({"%s"%antenna: None})

        return json.dumps(result)

resources_status_service = csrf_exempt(
    DjangoApplication(Application([ResourcesStatus],
                                  'cl.alma.arat.webservice.ResourcesStatus',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))