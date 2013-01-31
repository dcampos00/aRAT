from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String, Boolean
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

class checkConsistencyService(ServiceBase):
    @rpc(String, _returns=String)
    def check(ctx, debug):
        if debug:
            result = '<errors>'
            for i in xrange(5):
                result += '<error>CONSISTENCY ERROR # %s</error>'%(i)
            result += '</errors>'
            return result
        else:
            return 'SUCCESS'

check_consistency_service = csrf_exempt(DjangoApplication(Application([checkConsistencyService],
                                                                   'cl.alma.arat.webservice.checkConsistency',
                                                                   in_protocol=Soap11(),
                                                                   out_protocol=Soap11(),
                                                                   interface=Wsdl11(),
                                                                   )))
