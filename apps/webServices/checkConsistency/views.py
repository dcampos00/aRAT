from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import srpc

from aRAT.apps.home.models import (Antenna, PAD,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration,
                                   HolographyConfiguration)


class checkConsistencyService(ServiceBase):
    """
    Class that provide a web service, this web service
    expose a method check that check the consistency of all
    resources
    """
    @srpc(_returns=String)
    def check():
        """
        Method that provide the functionality of check the
        consistency in all resources.
        If exist some incosistency the method returns the errors
        in the next XML format:
            <errors>
               <error>ERROR 1 TEXT...</error>
               <error>ERROR 2 TEXT...</error>
               ...
            </errors>
        and if not exist inconsistencies the methos returns
        'SUCCESS'
        """

        _errors = []
        # is checked the consistency for the STE and Bands
        for antenna in Antenna.objects.all():
            if antenna.exist_errors():
                _e_text = "\n"
                for e in antenna.text_status():
                    _e_text += "%s\n" % e
                _errors.append(_e_text)

        # is checked the consistency for the PADs
        for pad in PAD.objects.all():
            if pad.exist_errors():  # if exist some error in the pad
                _e_text = "\n"
                # the list of string is passed as single string
                for e in pad.text_status():
                    _e_text += "%s\n" % e
                _errors.append(_e_text)

        # is checked the consistency for the Correlator Configurations
        for corr_conf in CorrelatorConfiguration.objects.all():
            if corr_conf.exist_errors():
                _e_text = "\n"
                for e in corr_conf.text_status():
                    _e_text += "%s\n" % e
                _errors.append(_e_text)

        # is checked the consistency for the CentralLO Configurations
        for clo_conf in CentralloConfiguration.objects.all():
            if clo_conf.exist_errors():
                _e_text = "\n"
                for e in clo_conf.text_status():
                    _e_text += "%s\n" % e
                _errors.append(_e_text)

        # is checked the consistency for the Holography Receptors
        for holo in HolographyConfiguration.objects.all():
            if holo.exist_errors():
                _e_text = "\n"
                for e in holo.text_status():
                    _e_text += "%s\n" % e
                _errors.append(_e_text)

        if not _errors:
            return 'SUCCESS'
        else:
            _result = '<errors>\n'
            for e in _errors:
                _result += '<error>%s</error>\n' % e
            _result += '</errors>'
            return _result

check_consistency_service = csrf_exempt(
    DjangoApplication(Application([checkConsistencyService],
                                  'cl.alma.arat.webservice.checkConsistency',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
