from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# models
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration, TableHeader
from aRAT.apps.common.models import Configuration
from django.conf import settings

# necessary imports to authenticate system
import logging
from django.contrib.auth import authenticate, login, logout

def login_user_view(request):
    """View to login in authenticate system"""

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
    """Logout View"""

    logout(request)
    return HttpResponseRedirect("/")

def home_view(request):
    """Home view"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    ctx = {'read_only': block_status.value}
    return render_to_response('home/index.djhtml', ctx, context_instance=RequestContext(request))

def ste_configuration_view(request):
    """View for STE configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    # if retrieved the block status of the current configuration
    block_status = Configuration.objects.get(setting='BLOCK')

    vendors = []
    stes = Antenna().STEs
    
    antennas = {}
    for antenna in Antenna.objects.all().order_by('name'):
        if not antenna.active:
            continue

        if antenna.vendor not in antennas:
            antennas.setdefault(antenna.vendor, [])
            vendors.append(antenna.vendor)
        antennas[antenna.vendor].append(antenna)

    # variables are passed to the view
    ctx = {'error': error,
           'read_only':block_status.value,
           'vendors': vendors,
           'stes':stes,
           'antennas': antennas
           }
    return render_to_response('home/ste.djhtml', ctx, context_instance=RequestContext(request))

def pad_configuration_view(request):
    """View for PAD configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()


    locations = []
    pads = {}

    for pad in PAD.objects.all().order_by('name'):
        if not pad.active:
            continue

        if pad.location not in pads:
            pads.setdefault(pad.location, [])
            locations.append(pad.location)
        pads[pad.location].append(pad)

    ctx = {'error': error,
           'read_only': block_status.value,
           'locations': locations,
           'pads':pads,
           'antennas':antennas
           }
    return render_to_response('home/pad.djhtml', ctx, context_instance=RequestContext(request))

def corr_configuration_view(request):
    """View for Correlator configuration"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    correlators = []
    corr_confs = {}

    for corr_config in CorrelatorConfiguration.objects.all():
        if not corr_config.active:
            continue

        if corr_config.correlator not in corr_confs:
            corr_confs.setdefault(corr_config.correlator, [])
            correlators.append(corr_config.correlator)
        corr_confs[corr_config.correlator].append(corr_config)

    ctx = {'error': error,
           'read_only': block_status.value,
           'correlators': correlators,
           'corr_confs': corr_confs,
           'antennas': antennas
           }
    return render_to_response('home/corr.djhtml', ctx, context_instance=RequestContext(request))


def clo_configuration_view(request):
    """View for CentralLO configuration"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    centrallos = []
    clo_confs = {}

    for clo_config in CentralloConfiguration.objects.all():
        if not clo_config.active:
            continue

        if clo_config.centrallo not in clo_confs:
            clo_confs.setdefault(clo_config.centrallo, [])
            centrallos.append(clo_config.centrallo)
        clo_confs[clo_config.centrallo].append(clo_config)

    ctx = {'error': error,
           'read_only': block_status.value,
           'centrallos': centrallos,
           'clo_confs': clo_confs,
           'antennas':antennas
           }
    return render_to_response('home/clo.djhtml', ctx, context_instance=RequestContext(request))

def holography_configuration_view(request):
    """View for Holography Receptor Configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    holos = []
    for holo in HolographyConfiguration.objects.all():
        if not holo.active:
            continue

        holos.append(holo)

    ctx = {'error': error,
           'read_only': block_status.value,
           'holos': holos,
           'antennas': antennas
           }
    return render_to_response('home/holography.djhtml', ctx, context_instance=RequestContext(request))
