import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from aRAT.apps.home.models import PAD, Antenna, STE, DRX, SAS_LLC
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

    result = "" # variable that save the resulting string
    modals = "" # variable that save a confirmation form by each request
    
#    debug = div_alert, ste_id, antenna_id

    # the resources are update
    if antenna_id != "":
        antenna = Antenna.objects.filter(id=antenna_id)
        if ste_id != "":
            antenna.update(requested_ste=STE.objects.get(id=ste_id))
        else:
            antenna.update(requested_ste=None)

    # get resources with a request
    requested_resources = Antenna.objects.exclude(current_ste=F('requested_ste')).exclude(requested_ste__isnull=True).order_by('name')

    for r in Antenna.objects.exclude(name='BLANK'):
        dajax.script('$("#btns_ant_%s a").removeClass("btn-success")'%(r.id))

    for r in requested_resources:
        result += alert('The %s will be <strong>Changed</strong> from %s to %s'%(r, r.current_ste, r.requested_ste), id_=r.id)
        modals += modal('confirm%s'%r.id, 'Cancel Request', 'Are you sure of cancel the change request of %s?'%r, 'Cancel Request', 'Dajaxice.aRAT.apps.home.ste_update_alerts(Dajax.process,{\'div_alert\':\'%s\', \'div_modal\':\'%s\', \'antenna_id\': %s});$(\'.modal\').modal(\'hide\');update(true);'%(div_alert, div_modal, r.id))
        dajax.add_css_class('#ant_%s_ste_%s'%(r.id, r.requested_ste.id), ['btn', 'btn-success'])

    dajax.assign(div_alert, 'innerHTML', result)
    dajax.assign(div_modal, 'innerHTML', modals)
    
#    dajax.assign('#debug', 'innerHTML', debug)
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
    
    blank_antenna = Antenna.objects.get(name='BLANK')

    result = "" # variable that save the resulting string
    modals = "" # variable that save a confirmation form by each request
    
    debug = ste, div_alert, div_modal, pad_id, antenna_id

    pad = PAD.objects

    # the resources are update
    if pad_id != "":
        pad_updated = pad.filter(id=pad_id)
        if antenna_id != "" and antenna_id != "NULL":
            pad_updated.update(requestedAntenna=Antenna.objects.get(id=antenna_id))
        elif antenna_id == "NULL":
            pad_updated.update(requestedAntenna=blank_antenna)
        elif antenna_id == "":
            pad_updated.update(requestedAntenna=None)

    # get resources with a request
    requested_pads = pad.exclude(currentAntenna=F('requestedAntenna')).exclude(requestedAntenna__isnull=True).order_by('name')
    requested_pads_by_ste = requested_pads.filter(ste__name__startswith=ste)

    for r in requested_pads_by_ste:
        problem = "" #variable that save a some possible problem that could happend
        if (r.currentAntenna == None or r.currentAntenna == blank_antenna) and r.requestedAntenna != blank_antenna:
            # is proved if exist another resource with the same antenna
            for rr in requested_pads:
                if r != rr and r.requestedAntenna == rr.requestedAntenna:
                    if problem != '':
                        problem += ','
                    problem += "%s"%(rr)

            if problem != '':
                problem = 'The Antenna have another PAD assigned (%s)'%(problem)
            result += alert('The %s will be <strong>Assigned</strong> to %s'%(r, r.requestedAntenna), problem=problem, id_=r.id)
            modals += modal('confirm%s'%r.id, 'Cancel Request', 'Are you sure of cancel the assignation request to %s?'%r, 'Cancel Request', 'Dajaxice.aRAT.apps.home.pad_update_alerts(Dajax.process,{\'ste\':\'%s\',\'div_alert\':\'%s\', \'div_modal\':\'%s\', \'pad_id\': %s});$(\'.modal\').modal(\'hide\');update(true);'%(ste, div_alert, div_modal, r.id))
        elif (r.currentAntenna != None or r.currentAntenna != blank_antenna) and r.requestedAntenna == blank_drx:
            result += alert('The %s will be <strong>Unassigned</strong> from %s'%(r, r.currentAntenna), id_=r.id)
            modals += modal('confirm%s'%r.id, 'Cancel Request', 'Are you sure of cancel the unassignation request to %s?'%r, 'Cancel Request', 'Dajaxice.aRAT.apps.home.pad_update_alerts(Dajax.process,{\'ste\':\'%s\',\'div_alert\':\'%s\', \'div_modal\':\'%s\', \'pad_id\': %s});$(\'.modal\').modal(\'hide\');update(true);'%(ste, div_alert, div_modal, r.id))
        elif r.currentAntenna != None:
            # is proved if exist another resource with the same antenna
            for rr in requested_resources:
                if r != rr and r.requestedAntenna == rr.requestedAntenna:
                    if problem != '':
                        problem += ','
                    problem += "%s"%(rr)

            if problem != '':
                problem = 'The Antenna have another %s assigned (%s)'%(resource_type_text, problem)
            result += alert('The %s will be <strong>Changed</strong> from %s to %s'%(r, r.currentAntenna, r.requestedAntenna), problem=problem, id_=r.id)
            modals += modal('confirm%s'%r.id, 'Cancel Request', 'Are you sure of cancel the change request to %s?'%r, 'Cancel Request', 'Dajaxice.aRAT.apps.home.pad_update_alerts(Dajax.process,{\'ste\':\'%s\',\'div_alert\':\'%s\', \'div_modal\':\'%s\', \'pad_id\': %s});$(\'.modal\').modal(\'hide\');update(true);'%(ste, div_alert, div_modal, r.id))

    dajax.assign(div_alert, 'innerHTML', result)
    dajax.assign(div_modal, 'innerHTML', modals)
    
    dajax.assign('#debug', 'innerHTML', debug)
    return dajax.json()

@dajaxice_register
def corr_update_alerts(request, div_alert, div_modal, caimap='', drxbbpr0_id='', drxbbpr1_id='', drxbbpr2_id='', drxbbpr3_id='', antenna_id=''):
    dajax = Dajax()

    # if the application is block the function does not anything
    if settings.objects.get(setting='BLOCK').value:
        return dajax.json()

    blank_drx = DRX.objects.get(name='BLANK')

    debug = div_alert, div_modal, caimap, drxbbpr0_id, drxbbpr1_id, drxbbpr2_id, drxbbpr3_id, antenna_id

    result = ""
    modals = ""

    if antenna_id != "" and antenna_id != "NULL":
        antenna = Antenna.objects.filter(id=antenna_id)
        #caimap assignament
        if caimap != "" and caimap != "NULL":
            antenna.update(requested_bl_caimap=caimap)
        elif caimap == "NULL":
            antenna.update(requested_bl_caimap=-1)
            drxbbpr0_id = "NULL"
            drxbbpr1_id = "NULL"
            drxbbpr2_id = "NULL"
            drxbbpr3_id = "NULL"
        else:
            antenna.update(requested_bl_caimap=None)

        #drxbbpr0 assignament
        if drxbbpr0_id != "" and drxbbpr0_id != "NULL":
            antenna.update(requested_drxbbpr0=DRX.objects.get(id=drxbbpr0_id))
        elif drxbbpr0_id == "NULL":
            antenna.update(requested_drxbbpr0=blank_drx)
        else:
            antenna.update(requested_drxbbpr0=None)

        #drxbbpr1 assignament
        if drxbbpr1_id != "" and drxbbpr1_id != "NULL":
            antenna.update(requested_drxbbpr1=DRX.objects.get(id=drxbbpr1_id))
        elif drxbbpr1_id == "NULL":
            antenna.update(requested_drxbbpr1=blank_drx)
        else:
            antenna.update(requested_drxbbpr1=None)

        #drxbbpr2 assignament
        if drxbbpr2_id != "" and drxbbpr2_id != "NULL":
            antenna.update(requested_drxbbpr2=DRX.objects.get(id=drxbbpr2_id))
        elif drxbbpr2_id == "NULL":
            antenna.update(requested_drxbbpr2=blank_drx)
        else:
            antenna.update(requested_drxbbpr2=None)

        #drxbbpr3 assignament
        if drxbbpr3_id != "" and drxbbpr3_id != "NULL":
            antenna.update(requested_drxbbpr3=DRX.objects.get(id=drxbbpr3_id))
        elif drxbbpr3_id == "NULL":
            antenna.update(requested_drxbbpr3=blank_drx)
        else:
            antenna.update(requested_drxbbpr3=None)

    # get resources with a request
    requested_resources = Antenna.objects.exclude(current_drxbbpr0=F('requested_drxbbpr0'), current_drxbbpr1=F('requested_drxbbpr1'), current_drxbbpr2=F('requested_drxbbpr2'), current_drxbbpr3=F('requested_drxbbpr3')).exclude(requested_drxbbpr0__isnull=True,requested_drxbbpr1__isnull=True, requested_drxbbpr2__isnull=True, requested_drxbbpr3__isnull=True).order_by('name')

    for r in requested_resources:
        alerts = {'assign_problem': [], 'assign': [], 'unassign': [], 'change': []}

        if (r.current_bl_caimap == None or r.current_bl_caimap == -1) and r.requested_bl_caimap != -1:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_bl_caimap == rr.requested_bl_caimap:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append(["CAIMAP %s"%r.requested_bl_caimap, res_problem])
            
            alerts['assign'].append("CAIMAP %s"%r.requested_bl_caimap)
        elif r.current_bl_caimap != None and r.current_bl_caimap != -1 and r.requested_bl_caimap == -1:
            alerts['unassign'].append("CAIMAP %s"%r.current_bl_caimap)
        elif r.current_bl_caimap != None:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_bl_caimap == rr.requested_bl_caimap:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append(["CAIMAP %s"%r.requested_bl_caimap, res_problem])

            alerts['change'].append("CAIMAP %s"%r.requested_bl_caimap)

        if (r.current_drxbbpr0 == None or r.current_drxbbpr0 == blank_drx) and r.requested_drxbbpr0 != blank_drx:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr0 == rr.requested_drxbbpr0:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr0, res_problem])
            
            alerts['assign'].append(r.requested_drxbbpr0)
        elif r.current_drxbbpr0 != None and r.current_drxbbpr0 != blank_drx and r.requested_drxbbpr0 == blank_drx:
            alerts['unassign'].append(r.current_drxbbpr0)
        elif r.current_drxbbpr0 != None:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr0 == rr.requested_drxbbpr0:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr0, res_problem])

            alerts['change'].append(r.requested_drxbbpr0)

        if (r.current_drxbbpr1 == None or r.current_drxbbpr1 == blank_drx) and r.requested_drxbbpr1 != blank_drx:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr1 == rr.requested_drxbbpr1:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr1, res_problem])
            
            alerts['assign'].append(r.requested_drxbbpr1)
        elif r.current_drxbbpr1 != None and r.current_drxbbpr1 != blank_drx and r.requested_drxbbpr1 == blank_drx:
            alerts['unassign'].append(r.current_drxbbpr1)
        elif r.current_drxbbpr1 != None:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr1 == rr.requested_drxbbpr1:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr0, res_problem])

            alerts['change'].append(r.requested_drxbbpr1)

        if (r.current_drxbbpr2 == None or r.current_drxbbpr2 == blank_drx) and r.requested_drxbbpr2 != blank_drx:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr2 == rr.requested_drxbbpr2:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr2, res_problem])
            
            alerts['assign'].append(r.requested_drxbbpr2)
        elif r.current_drxbbpr2 != None and r.current_drxbbpr2 != blank_drx and r.requested_drxbbpr2 == blank_drx:
            alerts['unassign'].append(r.current_drxbbpr2)
        elif r.current_drxbbpr2 != None:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr2 == rr.requested_drxbbpr2:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr2, res_problem])

            alerts['change'].append(r.requested_drxbbpr0)

        if (r.current_drxbbpr3 == None or r.current_drxbbpr3 == blank_drx) and r.requested_drxbbpr3 != blank_drx:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr3 == rr.requested_drxbbpr3:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr3, res_problem])
            
            alerts['assign'].append(r.requested_drxbbpr3)
        elif r.current_drxbbpr3 != None and r.current_drxbbpr3 != blank_drx and r.requested_drxbbpr3 == blank_drx:
            alerts['unassign'].append(r.current_drxbbpr3)
        elif r.current_drxbbpr3 != None:
            # is proved if exist another resource with the same antenna
            res_problem = []
            for rr in requested_resources:
                if r != rr and r.requested_drxbbpr3 == rr.requested_drxbbpr3:
                    res_problem.append(rr)

            if res_problem != []:
                alerts['assign_problem'].append([r.requested_drxbbpr3, res_problem])

            alerts['change'].append(r.requested_drxbbpr0)

        # is created the results
        assign = ""
        unassign = ""
        change = ""
        problem = ""
        if alerts['assign'] != []:
            first_loop = True
            for i in alerts['assign']:
                if not first_loop:
                    assign += ', '
                assign += '%s'%i
                first_loop = False
            assign = 'The %s will be <strong>Assigned</strong>'%assign
        if alerts['unassign'] != []:
            first_loop = True
            for i in alerts['unassign']:
                if not first_loop:
                    unassign += ', '
                unassign += '%s'%i
                first_loop = False
            unassign = 'The %s will be <strong>Unassigned</strong>'%assign
        if alerts['change'] != []:
            first_loop = True
            for i in alerts['change']:
                if not first_loop:
                    change += ', '
                change += '%s'%i
                first_loop = False
            change = 'The %s will be <strong>Changed</strong>'%change
        if alerts['assign_problem'] != []:
            p = ""
            for i in alerts['assign_problem']:
                res_problem = ""
                first_loop = True
                for r_problem in i[1]:
                    if not first_loop:
                        res_problem += ", "
                    res_problem += "%s"%r_problem
                    first_loop = False
                p += '<br/>The %s will be assigned to %s'%(i[0], res_problem)
            problem += p
            

        if alerts['assign'] != [] or alerts['unassign'] != [] or alerts['change'] != []:
            result += alert('%s%s%s to %s'%(assign, unassign, change, r), problem=problem, id_=r.id)
            modals += modal('confirm%s'%r.id, 'Cancel Request', 'Are you sure of cancel the request to %s?'%r, 'Cancel Request', 'Dajaxice.aRAT.apps.home.corr_update_alerts(Dajax.process,{\'div_alert\':\'%s\', \'div_modal\':\'%s\', \'antenna_id\': %s});$(\'.modal\').modal(\'hide\');update(true);'%(div_alert, div_modal, r.id))


    dajax.assign(div_alert, 'innerHTML', result)
    dajax.assign(div_modal, 'innerHTML', modals)
    
    dajax.assign('#debug', 'innerHTML', debug)
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
