from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# are imported the models of the application
from aRAT.apps.home.models import (Antenna, PAD,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration,
                                   HolographyConfiguration)
# is imported the model that contains all the configurations
from aRAT.apps.common.models import Configuration

# necessary imports to authenticate system
from django.contrib.auth import authenticate, login, logout


def read_only(request):
    """
    Return *True* if a request is the application
    is in read only mode for the user
    """
    block_status = Configuration.objects.get(setting='BLOCK').value
    is_requester = request.user.groups.filter(name='Requester')

    return block_status or not is_requester


def status_message(request):
    status_message = {'type': None,
                      'text': None}
    if read_only(request):
        status_message['type'] = 'alert-error'
        if request.user.groups.filter(name='Requester'):
            status_message['text'] = ('aRAT is blocked, '
                                      'Is not possible do changes.')
        else:
            status_message['text'] = ('aRAT is unblocked, '
                                      'You aren\'t an authorized requester.')
    else:
        status_message['type'] = 'alert-success'
        status_message['text'] = ('aRAT is unblocked, '
                                  'Is possible do changes.')

    return status_message


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
    return render_to_response('home/login.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def logout_user_view(request):
    """Logout View"""

    # the user is logout
    logout(request)
    return HttpResponseRedirect("/")


def home_view(request):
    """
    Home view, That view is an overview of the current
    status of the system
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    ctx = {'read_only': read_only(request),
           'status_message': status_message(request)}
    return render_to_response('home/index.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def ste_configuration_view(request):
    """View for STE configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

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
           'status_message': status_message(request),
           'read_only': read_only(request),
           'vendors': vendors,
           'stes': stes,
           'antennas': antennas
           }
    return render_to_response('home/ste.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def band_configuration_view(request):
    """View for Band Configurations"""
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    # the bands values are created
    bands = [i for i in xrange(1, 11)]
    vendors = []
    antennas = {}
    for antenna in Antenna.objects.all().order_by('name'):
        if not antenna.active:
            continue

        if antenna.vendor not in antennas:
            antennas.setdefault(antenna.vendor, [])
            vendors.append(antenna.vendor)
        antennas[antenna.vendor].append(antenna)

    ctx = {'error': error,
           'status_message': status_message(request),
           'read_only': read_only(request),
           'vendors': vendors,
           'bands': bands,
           'antennas': antennas
           }

    return render_to_response('home/band.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def pad_configuration_view(request):
    """View for PAD configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

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
           'status_message': status_message(request),
           'read_only': read_only(request),
           'locations': locations,
           'pads': pads,
           'antennas': antennas
           }

    return render_to_response('home/pad.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def corr_configuration_view(request):
    """View for Correlator configuration"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

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
           'status_message': status_message(request),
           'read_only': read_only(request),
           'correlators': correlators,
           'corr_confs': corr_confs,
           'antennas': antennas
           }
    return render_to_response('home/corr.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def clo_configuration_view(request):
    """View for CentralLO configuration"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

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
           'status_message': status_message(request),
           'read_only': read_only(request),
           'centrallos': centrallos,
           'clo_confs': clo_confs,
           'antennas': antennas
           }
    return render_to_response('home/clo.djhtml',
                              ctx,
                              context_instance=RequestContext(request))


def holography_configuration_view(request):
    """View for Holography Receptor Configurations"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    holos = []
    for holo in HolographyConfiguration.objects.all():
        if not holo.active:
            continue

        holos.append(holo)

    ctx = {'error': error,
           'status_message': status_message(request),
           'read_only': read_only(request),
           'holos': holos,
           'antennas': antennas
           }

    return render_to_response('home/holography.djhtml',
                              ctx,
                              context_instance=RequestContext(request))
