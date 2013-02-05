import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from aRAT.apps.home.models import Antenna, PAD
from django.db.models import F, Q

from aRAT.apps.common.models import settings as app_settings


@dajaxice_register
def ste_update_alerts(request, ste_id='', antenna_id=''):
    """
    Function that allow keep update the requests for pads

    Arguments:
    - `ste_id`:
    - `antenna_id`:
    """

    dajax = Dajax() # object that manage the AJAX connection
    
    # if the application is block the function does not anything
    if app_settings.objects.get(setting='BLOCK').value:
        return dajax.json()

    # first the antenna information is updated
    if antenna_id != '':
        antenna = Antenna.objects.get(id=antenna_id)
        if ste_id != '' and ste_id != antenna.current_ste:
            antenna.requested_ste = ste_id
        else:
            antenna.requested_ste = None
        antenna.save()

    # is loaded all current status of the ste configuration
    antennas = Antenna.objects.all()
    for antenna in antennas:
        dajax.add_data({'antenna': {'id': antenna.id, 'name': antenna.name},
                        'ste': {'id': antenna.requested_ste, 'name': antenna.get_requested_ste_display()}},
                       'update_status')

    return dajax.json()

@dajaxice_register
def pad_update_alerts(request, pad_id='', antenna_id=''):
    """
    Function that allow keep update the alerts for pads if tf... STEs

    Arguments:
    - `pad_id`: id value of a pad that will be requested
    - `antenna_id`: id value of an antenna that will be assigned to a pad
    """

    dajax = Dajax()

    # if the application is block the function does not anything
    if app_settings.objects.get(setting='BLOCK').value:
        return dajax.json()
    
    # first the pad information is updated
    if pad_id != '':
        pad = PAD.objects.get(id=pad_id)
        if antenna_id != '' and pad.current_antenna != Antenna.objects.get(id=antenna_id):
            pad.requested_antenna = Antenna.objects.get(id=antenna_id)
        else:
            pad.requested_antenna = None
        pad.save()

    # is loaded all current status of the ste configuration
    pads = PAD.objects.all()
    for pad in pads:

        pad_errors = []
        if pad.requested_antenna != None:
            for pad2 in PAD.objects.all():
                if pad != pad2:
                    if pad.requested_antenna == pad2.requested_antenna:
                        pad_errors.append(pad2.name)
                    elif pad.requested_antenna == pad2.current_antenna:
                        pad_errors.append(pad2.name)
                    

        current_antenna_name = current_antenna_id = None
        requested_antenna_name = requested_antenna_id = None

        if pad.current_antenna:
            current_antenna_name = pad.current_antenna.name
            current_antenna_id = pad.current_antenna_id
        if pad.requested_antenna:
            requested_antenna_name = pad.requested_antenna.name
            requested_antenna_id = pad.requested_antenna.id

        dajax.add_data({'pad': {'id': pad.id, 'name': pad.name},
                        'current_antenna': {'id': current_antenna_name, 'name': current_antenna_name},
                        'requested_antenna': {'id': requested_antenna_id, 'name': requested_antenna_name},
                        'error': [e for e in pad_errors]
                        },
                       'update_status')

    return dajax.json()

@dajaxice_register
def corr_update_alerts(request, div_alert, div_modal, caimap='', drxbbpr0_id='', drxbbpr1_id='', drxbbpr2_id='', drxbbpr3_id='', antenna_id=''):
    dajax = Dajax()

    # if the application is block the function does not anything
    if app_settings.objects.get(setting='BLOCK').value:
        return dajax.json()

    return dajax.json()
