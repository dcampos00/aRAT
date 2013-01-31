from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String, Boolean
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

class changesPageService(ServiceBase):
    @rpc(String, _returns=String)
    def changes(ctx, debug):
        if debug:
            return 'FAILURE'
        else:
            result = '<changes>'
            for i in xrange(10):
                result += '<change>CHANGE # %s</change>'%(i)
            result += '</changes>'
            return result

changes_page_service = csrf_exempt(DjangoApplication(Application([changesPageService],
                                                                   'cl.alma.arat.webservice.changesPage',
                                                                   in_protocol=Soap11(),
                                                                   out_protocol=Soap11(),
                                                                   interface=Wsdl11(),
                                                                   )))
