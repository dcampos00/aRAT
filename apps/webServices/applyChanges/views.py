from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String, Boolean
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

from datetime import datetime

from aRAT.apps.home.models import History, Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration
from aRAT.apps.webServices.checkConsistency.views import checkConsistencyService

class applyChangesService(ServiceBase):
    """
    Class that provide a web service, that expose a method that allow apply
    the requested to the database
    """
    @rpc(_returns=String)
    def apply(ctx):
        """
        Method that apply the requested changes permanently to the database
        i.e. pass the requested configurations to current configurations

        Also this method stores the request text in the DB
        """

        if checkConsistencyService.check(ctx) != 'SUCCESS':
            return 'FAILURE'

        _request_text = ""

        # is applied the chanes for the Antennas
        for antenna in Antenna.objects.all():
            # if exist a request and the 
            if antenna.active and antenna.requested_ste != antenna.current_ste:
                for status in antenna.text_status():
                    _request_text += "%s\n"%status
                
                # is saved the requested ste to current ste
                antenna.current_ste = antenna.requested_ste

                # is cleaned the request data
                antenna.requested_ste = None
                antenna.requester = None
                antenna.request_date = None

                # is saved the information
                antenna.save()

        # is applied the chanes for the PADs
        for pad in PAD.objects.all():
            # if exist a request
            if pad.active and pad.requested_antenna is not None:
                for status in pad.text_status():
                    _request_text += "%s\n"%status

                pad.current_antenna = pad.requested_antenna
                pad.requested_antenna = None
                pad.assigned = True
                pad.requester = None
                pad.request_date = None
                pad.save()

        # is applied the chanes for the Correlator Configurations
        for corr_conf in CorrelatorConfiguration.objects.all():
            if corr_conf.active and corr_conf.requested_antenna is not None:
                for status in corr_conf.text_status():
                    _request_text += "%s\n"%status

                corr_conf.current_antenna = corr_conf.requested_antenna
                corr_conf.requested_antenna = None
                corr_conf.assigned = True
                corr_conf.requester = None
                corr_conf.request_date = None
                corr_conf.save()

        # is applied the chanes for the CentralLO Configurations
        for clo_conf in CentralloConfiguration.objects.all():
            if clo_conf.active and clo_conf.requested_antenna is not None:
                for status in clo_conf.text_status():
                    _request_text += "%s\n"%status

                clo_conf.current_antenna = clo_conf.requested_antenna
                clo_conf.requested_antenna = None
                clo_conf.assigned = True
                clo_conf.requester = None
                clo_conf.request_date = None
                clo_conf.save()

        # is applied the chanes for the Holography Receptors
        for holo in HolographyConfiguration.objects.all():
            if holo.active and holo.requested_antenna is not None:
                for status in holo.text_status():
                    _request_text += "%s\n"%status

                holo.current_antenna = holo.requested_antenna
                holo.requested_antenna = None
                holo.assigned = True
                holo.requester = None
                holo.request_date = None
                holo.save()

        #is saved the request in the DB
        _request_history = History()
        _request_history.date_time = datetime.now()
        _request_history.request = _request_text
        _request_history.save()


        return 'SUCCESS'

apply_changes_service = csrf_exempt(
    DjangoApplication(Application([applyChangesService],
                                  'cl.alma.arat.webservice.applyChanges',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
