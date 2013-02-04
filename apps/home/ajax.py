import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from aRAT.apps.home.models import Antenna
from django.db.models import F, Q

from aRAT.apps.common.models import settings


@dajaxice_register
def ste_update_alerts(request, div_alert, div_modal, ste_id='', antenna_id=''):
    """
    Function that allow keep update the alerts for pads if tf... STEs

    Arguments:
    - `div_alert`: place where the alerts will be placed (e.g: #div_alert)
    - `pad`: id value of a pad that will be requested
    - `antenna`: id value of an antenna that will be assigned to a pad
    """

    dajax = Dajax() # object that manage the AJAX connection
    
    # if the application is block the function does not anything
    if settings.objects.get(setting='BLOCK').value:
        return dajax.json()

    return dajax.json()

@dajaxice_register
def pad_update_alerts(request, ste, div_alert, div_modal, pad_id='', antenna_id=''):
    """
    Function that allow keep update the alerts for pads if tf... STEs

    Arguments:
    - `div_alert`: place where the alerts will be placed (e.g: #div_alert)
    - `pad`: id value of a pad that will be requested
    - `antenna`: id value of an antenna that will be assigned to a pad
    """

    dajax = Dajax()

    # if the application is block the function does not anything
    if settings.objects.get(setting='BLOCK').value:
        return dajax.json()
    
    return dajax.json()

@dajaxice_register
def corr_update_alerts(request, div_alert, div_modal, caimap='', drxbbpr0_id='', drxbbpr1_id='', drxbbpr2_id='', drxbbpr3_id='', antenna_id=''):
    dajax = Dajax()

    # if the application is block the function does not anything
    if settings.objects.get(setting='BLOCK').value:
        return dajax.json()

    return dajax.json()

def alert(body='', title='', alert_type='alert-success', problem='', id_=''):
    """
    Function that return an alert in HTML bootstrap format

    Arguments:
    - `body`: body text of the alert
    - `title`: title in the alert
    - `alert_type`: Type of alert that will be generate (alert-error, alert-success, alert-info)
    - `problem`: possible text about a problem
    """

    # if the title is not empty this is highlighted
    if title != '':
        title = '<strong>%s</strong>'%title

    # if exist some problem the alert_type is changed to alert-error
    if problem != '':
        alert_type = 'alert-error'
        problem = '.<br><strong>ERROR!</strong> '+problem

    return '<div class="row-fluid"><div class="alert %s span12"><a onclick="update(false);$(\'#confirm%s\').modal(\'show\');" role="button" class="close">&times;</a>%s %s%s</div></div>'%(alert_type, id_, title, body, problem);

def modal(modal_id='', title='', body='', button_confirm_text='Confirm', button_confirm_action='', button_confirm_type='btn-danger'):
    return '<div id="%s" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="confirmHeader" aria-hidden="true"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="update(true);">&times;</button><h3 id="confirmHeader">%s</h3></div><div class="modal-body"><p>%s</p></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true" onclick="update(true);">Close</button><button class="btn %s" onclick="%s">%s</button></div></div>'%(modal_id, title, body, button_confirm_type, button_confirm_action, button_confirm_text)
