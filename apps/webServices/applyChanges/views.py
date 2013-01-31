from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String, Boolean
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

class applyChangesService(ServiceBase):
    """
    Class that provide a web service, that expose a method that allow apply
    the requested to the database
    """
    @rpc(String, _returns=String)
    def apply(ctx, debug):
        """
        Method that apply the requested changes permanently to the database

        Arguments:
        - `debug`: this argument allow debug the exposed method returning 
        FAILURE
        """
        if debug:
            return 'FAILURE'
        else:
            return 'SUCCESS'

apply_changes_service = csrf_exempt(DjangoApplication(Application([applyChangesService],
                                                                   'cl.alma.arat.webservice.applyChanges',
                                                                   in_protocol=Soap11(),
                                                                   out_protocol=Soap11(),
                                                                   interface=Wsdl11(),
                                                                   )))
