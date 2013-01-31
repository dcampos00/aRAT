# Create your views here.

# import logging

from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String, Boolean
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

from aRAT.apps.common.models import settings

class blockUnblockService(ServiceBase):
    @rpc(String, _returns=String)
    def block(ctx, debug):
        # update settings to block
        settings.objects.filter(setting='BLOCK').update(value=True)
        if debug:
            return 'FAILURE'
        else:
            return 'SUCCESS'

    @rpc(String, _returns=String)
    def unblock(ctx, debug):
        settings.objects.filter(setting='BLOCK').update(value=False)
        if debug:
            return 'FAILURE'
        else:
            return 'SUCCESS'

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
block_unblock_service = csrf_exempt(DjangoApplication(Application([blockUnblockService],
                                                                   'cl.alma.arat.webservice.blockUnblock',
                                                                   in_protocol=Soap11(),
                                                                   out_protocol=Soap11(),
                                                                   interface=Wsdl11(),
                                                                   )))
