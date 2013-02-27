from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc

from aRAT.apps.home.models import (PAD, Antenna,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration,
                                   HolographyConfiguration)


class changesPageService(ServiceBase):
    """
    Class that expose the method changes, this method
    returns a XML with the changes made in the latest request
    """
    @rpc(_returns=String)
    def changes(ctx):
        """Return a string with the XML of the last changes"""
        # is loaded the last request from the DB
        result = "<changes>"

        # is created the XML
        for antenna in Antenna.objects.all():
            if not antenna.active:
                continue

            if antenna.is_requested():
                result += "\n<change>\n"
                for line in antenna.text_status():
                    result += "%s\n" % line
                result += "</change>"

        for pad in PAD.objects.all():
            if not pad.active:
                continue

            if pad.is_requested():
                result += "\n<change>\n"
                for line in pad.text_status():
                    result += "%s\n" % line
                result += "</change>"

        for corr_conf in CorrelatorConfiguration.objects.all():
            if not corr_conf.active:
                continue

            if corr_conf.is_requested():
                result += "\n<change>\n"
                for line in corr_conf.text_status():
                    result += "%s\n" % line
                result += "</change>"

        for clo_conf in CentralloConfiguration.objects.all():
            if not corr_conf.active:
                continue

            if clo_conf.is_requested():
                result += "\n<change>\n"
                for line in clo_conf.text_status():
                    result += "%s\n" % line
                result += "</change>"

        for holo in HolographyConfiguration.objects.all():
            if not holo.active:
                continue

            if holo.is_requested():
                result += "\n<change>\n"
                for line in holo.text_status():
                    result += "%s\n" % line
                result += "</change>"

        result += "</changes>"

        return result

changes_page_service = csrf_exempt(
    DjangoApplication(Application([changesPageService],
                                  'cl.alma.arat.webservice.changesPage',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
