from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# models
from aRAT.apps.home.models import Antenna, PAD, Correlator, CentralLO
from aRAT.apps.common.models import settings as app_settings
from django.conf import settings

# necessary imports to authenticate system
import logging
from django.contrib.auth import authenticate, login, logout

def login_user_view(request):
    """
    View to login in authenticate system
    """

    state = 'Please login with your Username and Password.'
    username = password = ''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = request.POST

        username = form['username'].strip()
        password = form['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            state = 'Your username and/or password were incorrect.'

    ctx = {'state': state, 'username': username}
    return render_to_response('home/login.djhtml', ctx, context_instance=RequestContext(request))

def logout_user_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def home_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = app_settings.objects.get(setting='BLOCK')
    ctx = {'read_only': block_status.value}
    return render_to_response('home/index.djhtml', ctx, context_instance=RequestContext(request))

def ste_configuration_view(request):
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = app_settings.objects.get(setting='BLOCK')

    vendors = [i.strip().replace('-',' ') for i in open(settings.CONFIGURATION_DIR+'vendors.cfg').readlines() if i.strip()]
    stes = Antenna().STEs
#    stes = [i.strip().split()[0] for i in open('aRAT/configuration/stes.cfg').readlines() if i.strip()]
    
    antennas = [(v.replace('-', ' '), []) for v in vendors]
    antennas = dict(v for v in antennas)

    for name_antenna in open(settings.CONFIGURATION_DIR+'antennas.cfg').readlines():
        name_antenna.strip()
        if name_antenna:
            name_antenna, vendor = name_antenna.split()
            vendor = vendor.replace('-', ' ')

            if Antenna.objects.filter(name=name_antenna):
                antenna = Antenna.objects.get(name=name_antenna)
                antennas[vendor].append(antenna)
            else:
                for ste in stes:
                    if 'VENDOR' in ste:
                        default_ste = ste[0]
                        break
                    else:
                        error = 'The Vendor STE does not exist.'

                new_antenna = Antenna(name=name_antenna, current_ste=default_ste)
                new_antenna.save()
                antennas[vendor].append(new_antenna)

    # variables are passed to the view
    ctx = {'error': error,
           'read_only':block_status.value,
           'vendors': vendors,
           'stes':stes,
           'antennas': antennas
           }
    return render_to_response('home/ste.djhtml', ctx, context_instance=RequestContext(request))

def pad_configuration_view(request):
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = app_settings.objects.get(setting='BLOCK')

    locations = [i.strip() for i in open(settings.CONFIGURATION_DIR+'locations.cfg').readlines() if i.strip()]
    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    pads = [(l, []) for l in locations]
    pads = dict(l for l in pads)

    for pad in open(settings.CONFIGURATION_DIR+'pads.cfg').readlines():
        pad = pad.strip()
        if pad:
            pad_name, location = pad.split()
            if PAD.objects.filter(name=pad_name):
                pad = PAD.objects.get(name=pad_name)
                pads[location].append(pad)
            else:
                new_pad = PAD(name=pad_name)
                new_pad.save()
                pads[location].append(new_pad)

    ctx = {'error': error,
           'read_only': block_status.value,
           'locations': locations,
           'pads':pads,
           'antennas':antennas
           }
    return render_to_response('home/pad.djhtml', ctx, context_instance=RequestContext(request))

def corr_configuration_view(request):
    """
    View to configure the correlators
    """
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = app_settings.objects.get(setting='BLOCK')

    correlators = [i.strip() for i in open(settings.CONFIGURATION_DIR+'correlators.cfg').readlines() if i.strip()]
    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    corrs = [(c, []) for c in correlators]
    corrs = dict(c for c in corrs)

    for line_number, corr in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
        corr.strip()
        if corr:
            line = corr.split()
            line[0:-1] = [x.replace('-', ' ') for x in line[0:-1]]
            if Correlator.objects.filter(line=line_number):
                corr = Correlator.objects.get(line=line_number)
                corrs[line[-1]].append(corr)
            else:
                new_corr = Correlator(line=line_number)
                new_corr.save()
                corrs[line[-1]].append(new_corr)

    ctx = {'error': error,
           'read_only': block_status.value,
           'correlators': correlators,
           'corrs': corrs,
           'antennas': antennas
           }
    return render_to_response('home/corr.djhtml', ctx, context_instance=RequestContext(request))


def clo_configuration_view(request):
    """
    View to configure the correlators
    """
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = app_settings.objects.get(setting='BLOCK')

    centrallos = [i.strip() for i in open(settings.CONFIGURATION_DIR+'centrallos.cfg').readlines() if i.strip()]
    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    clos = [(c, []) for c in centrallos]
    clos = dict(c for c in clos)

    for line_number, clo in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg')):
        clo.strip()
        if clo:
            line = clo.split()
            line[0:-1] = [x.replace('-', ' ') for x in line[0:-1]]
            if CentralLO.objects.filter(line=line_number):
                clo = CentralLO.objects.get(line=line_number)
                clos[line[-1]].append(clo)
            else:
                new_clo = CentralLO(line=line_number)
                new_clo.save()
                clos[line[-1]].append(new_clo)

    ctx = {'error': error,
           'read_only': block_status,
           'centrallos': centrallos,
           'clos': clos,
           'antennas':antennas
           }
    return render_to_response('home/clo.djhtml', ctx, context_instance=RequestContext(request))

