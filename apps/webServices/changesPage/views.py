from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne.model.primitive import String
from spyne.service import ServiceBase
from spyne.interface.wsdl import Wsdl11
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.application import Application
from spyne.decorator import rpc

from aRAT.apps.home.models import History

import re

class changesPageService(ServiceBase):
    """Class that expose the method changes, this method
    returns a XML with the changes made in the lastest request
    """
    @rpc(_returns=String)
    def changes(ctx):
        """Return a string with the XML of the last changes"""
        # is loaded the last request from the DB
        request = History.objects.reverse()[:1][0].request
        request = request.split('\n')

        result = "<changes>"
        
        # is created the XML
        _open = False
        for r in request:
            if not _open and r: # if r is not empty
                result += "\n<change>\n"
                _open = True
            result += "%s\n"%r
            if re.match("-- Request", r) is not None:
                result += "</change>"
                _open = False

        result += "</changes>"

        return result
#        if debug:
#            return 'FAILURE'
#        else:
#            result = '<changes>'
#            for i in xrange(10):
#                result += '<change>CHANGE # %s</change>'%(i)
#            result += '</changes>'
#            return result

changes_page_service = csrf_exempt(
    DjangoApplication(Application([changesPageService],
                                  'cl.alma.arat.webservice.changesPage',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))
