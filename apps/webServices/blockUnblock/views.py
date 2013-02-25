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

        The method return *FAILURE* if the *BLOCK* configuration does not exist
        and return *SUCCESS* if the application is blocked.
        """
        # is proved if exists the configuration in the DB
        if Configuration.objects.filter(setting='BLOCK') is None:
            return 'FAILURE'
        else:
            # the block configuration is update to true
            block = Configuration.objects.get(setting='BLOCK')
            block.value = True
            block.save()
            return 'SUCCESS'

    @rpc(_returns=String)
    def unblock(ctx):
        """
        Method that unblock the application changing the BLOCK setting
        in the DB

        The method return *FAILURE* if the *BLOCK* configuration does
        not exist and return *SUCCESS* if the application is unblocked
        successfully
        """
        # is proved if exists the configuration in the DB
        if Configuration.objects.filter(setting='BLOCK') is None:
            return 'FAILURE'
        else:
            # the block configuratios is updated to false
            block = Configuration.objects.get(setting='BLOCK')
            block.value = False
            block.save()
            return 'SUCCESS'

block_unblock_service = csrf_exempt(
    DjangoApplication(Application([blockUnblockService],
                                  'cl.alma.arat.webservice.blockUnblock',
                                  in_protocol=Soap11(),
                                  out_protocol=Soap11(),
                                  interface=Wsdl11(),
                                  )))


from django.http import HttpResponse, HttpResponseRedirect


def block_app_view(request):
    """
    Function that provide a view that allows to have access
    to the blockUnblock web service, to block the application

    Note: The view is used in the administration panel
    """
    if request.method == "POST":
        form = request.POST
        if eval(form['block']):
            blockUnblockService.block("")

            return HttpResponseRedirect("/admin")

    return HttpResponse('Error!')


def unblock_app_view(request):
    """
    Function that provide a view that allows to have access
    to the blockUnblock web service, to unblock the application

    Note: The view is used in the administration panel
    """

    if request.method == "POST":
        form = request.POST
        if not eval(form['block']):
            blockUnblockService.unblock("")

            return HttpResponseRedirect("/admin")

    return HttpResponse('Error!')
