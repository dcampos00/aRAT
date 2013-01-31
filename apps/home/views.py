from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# models
from aRAT.apps.home.models import PAD, Antenna, STE, DRX, SAS_LLC
from aRAT.apps.common.models import settings

# necessary imports to authenticate system
import logging
from django.contrib.auth import authenticate, login, logout

# forms
from aRAT.apps.home.forms import LoginForm, STEForm

def login_user_view(request):
    """
    View to login in authenticate system
    """

    state = 'Please login with your Username and Password.'
    username = password = ''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                state = 'Your username and/or password were incorrect.'

    else:
        form = LoginForm()

    ctx = {'state': state, 'username': username, 'form': form}
    return render_to_response('home/login.djhtml', ctx, context_instance=RequestContext(request))

def logout_user_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def home_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = settings.objects.get(setting='BLOCK')
    ctx = {'read_only': block_status.value}
    return render_to_response('home/index.djhtml', ctx, context_instance=RequestContext(request))

def pad_configuration_view(request):
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = settings.objects.get(setting='BLOCK')

    locations = [i.strip() for i in open('aRAT/configuration/locations.cfg').readlines() if i.strip()]
    antennas = [i.strip().split()[0] for i in open('aRAT/configuration/antennas.cfg').readlines() if i.strip()]

    pads = {l:[] for l in locations}
    for pad in open('aRAT/configuration/pads.cfg').readlines():
        pad.strip()
        if pad:
            pad, location = pad.split()
            pads[location].append(pad)

    ctx = {'error': error,
           'read_only': block_status.value,
           'locations': locations,
           'pads':pads,
           'antennas':antennas
           }
    return render_to_response('home/pad.djhtml', ctx, context_instance=RequestContext(request))

def ste_configuration_view(request):
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = settings.objects.get(setting='BLOCK')

    vendors = [i.strip() for i in open('aRAT/configuration/vendors.cfg').readlines() if i.strip()]
    stes = [i.strip().split()[0] for i in open('aRAT/configuration/stes.cfg').readlines() if i.strip()]
    
    antennas = {v:[] for v in vendors}
    for antenna in open('aRAT/configuration/antennas.cfg').readlines():
        antenna.strip()
        if antenna:
            antenna, vendor = antenna.split()
            antennas[vendor].append(antenna)

    # variables are passed to the view
    ctx = {'error': error,
           'read_only':block_status.value,
           'vendors': vendors,
           'stes':stes,
           'antennas': antennas
           }
    return render_to_response('home/ste.djhtml', ctx, context_instance=RequestContext(request))

def corr_configuration_view(request):
    """
    View to configure the correlators
    """
    # variable error is defined
    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = settings.objects.get(setting='BLOCK')

    correlators = [i.strip() for i in open('aRAT/configuration/correlators.cfg').readlines() if i.strip()]
    antennas = [i.strip().split()[0] for i in open('aRAT/configuration/antennas.cfg').readlines() if i.strip()]
    corrs = {c:[] for c in correlators}

    for corr in open('aRAT/configuration/corr.cfg').readlines():
        corr.strip()
        if corr:
            line = corr.split()
            corrs[line[-1]].append(line[0:-1])

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

    block_status = settings.objects.get(setting='BLOCK')

    centrallos = [i.strip() for i in open('aRAT/configuration/centrallos.cfg').readlines() if i.strip()]
    antennas = [i.strip().split()[0] for i in open('aRAT/configuration/antennas.cfg').readlines() if i.strip()]
    clos = {c:[] for c in centrallos}

    for clo in open('aRAT/configuration/clo.cfg').readlines():
        clo.strip()
        if clo:
            line = clo.split()
            clos[line[-1]].append(line[0:-1])

    ctx = {'error': error,
           'read_only': block_status,
           'centrallos': centrallos,
           'clos': clos,
           'antennas':antennas
           }
    return render_to_response('home/clo.djhtml', ctx, context_instance=RequestContext(request))

