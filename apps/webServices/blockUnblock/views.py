# Create your views here.

# import logging

from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

from aRAT.apps.common.models import Configuration

class blockUnblockService(ServiceBase):
    """
    Web services that allow block and unblock the application.
    This class expose two method one for block and one for unblock
    """
    @rpc(_returns=String)
    def block(ctx):
        """
        Method that block the application changing the BLOCK setting in the DB
        """
        # is proved if exists the configuration in the DB
        if Configuration.objects.filter(setting='BLOCK') == None:
            return 'FAILURE'
        else:
            # the block configuration is update to true
            Configuration.objects.get(setting='BLOCK').update(value=True)
            return 'SUCCESS'

    @rpc(_returns=String)
    def unblock(ctx):
        """
        Method that unblock the application changing the BLOCK setting in the DB
        """
        # is proved if exists the configuration in the DB
        if Configuration.objects.filter(setting='BLOCK') == None:
            return 'FAILURE'
        else:
            # the block configuratios is updated to false
            Configuration.objects.get(setting='BLOCK').update(value=False)
            return 'SUCCESS'

block_unblock_service = csrf_exempt(
    DjangoApplication(Application([blockUnblockService],
                                  'cl.alma.arat.webservice.blockUnblock',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
