from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# models
from aRAT.apps.home.models import Antenna, PAD, CorrelatorConfiguration, CentralloConfiguration, HolographyConfiguration
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

#    locations = [i.strip() for i in open(settings.CONFIGURATION_DIR+'locations.cfg').readlines() if i.strip()]

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()


    locations = []
    pads = {}

    for pad in PAD.objects.all().order_by('name'):
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

#    correlators = [i.strip() for i in open(settings.CONFIGURATION_DIR+'correlators.cfg').readlines() if i.strip()]

    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    # the correlator configurations are loaded, this are separated by location
    # for this the correlator configurations are loaded in a dictionary
#    corrs = [(c, []) for c in correlators]
#    corrs = dict(c for c in corrs)

#    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
#        line_string = line_string.strip()
#        if line_string:
#            line_list = line_string.split()
#            line_list[0:-1] = [x.replace('-', ' ') for x in line_list[0:-1]]
#            if line_string[0] == "#":
 #               corrs[line_list[-1]].append(line_list[0:-1])
 #           else:
#                if CorrelatorConfiguration.objects.filter(line=line_number):
#                    corr_config = CorrelatorConfiguration.objects.get(line=line_number)
#                    if corr_config.active:
#                        corrs[line_list[-1]].append(corr_config)
#                else:
#                    new_corr_config = CorrelatorConfiguration(line=line_number)
#                    new_corr_config.save()
#                    corrs[line_list[-1]].append(new_corr_config)

    correlators = []
    corr_confs = {}

    ctx = {'error': error,
           'read_only': block_status.value,
           'correlators': correlators,
           'corrs': corr_confs,
           'antennas': antennas
           }
    return render_to_response('home/corr.djhtml', ctx, context_instance=RequestContext(request))


def clo_configuration_view(request):
    """View for CentralLO configuration"""

    error = ''

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    block_status = Configuration.objects.get(setting='BLOCK')

    centrallos = [i.strip() for i in open(settings.CONFIGURATION_DIR+'centrallos.cfg').readlines() if i.strip()]
    # the antennas are loaded from the db
    antennas = Antenna.objects.all()

    clos = [(c, []) for c in centrallos]
    clos = dict(c for c in clos)

    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg')):
        line_string = line_string.strip()
        if line_string:
            line_list = line_string.split()
            line_list[0:-1] = [x.replace('-', ' ') for x in line_list[0:-1]]
            if line_string[0] == "#":
                clos[line_list[-1]].append(line_list[0:-1])
            else:
                if CentralloConfiguration.objects.filter(line=line_number):
                    clo_config = CentralloConfiguration.objects.get(line=line_number)
                    clos[line_list[-1]].append(clo_config)
                else:
                    new_clo_config = CentralloConfiguration(line=line_number)
                    new_clo_config.save()
                    clos[line_list[-1]].append(new_clo_config)

    ctx = {'error': error,
           'read_only': block_status.value,
           'centrallos': centrallos,
           'clos': clos,
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
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'holography.cfg')):
        line_string = line_string.strip()
        if line_string:
            holo = line_string
            if HolographyConfiguration.objects.filter(line=line_number):
                holo_config = HolographyConfiguration.objects.get(line=line_number)
                holos.append(holo_config)
            else:
                new_holo_config = HolographyConfiguration(line=line_number)
                new_holo_config.save()
                holos.append(new_holo_config)

    ctx = {'error': error,
           'read_only': block_status.value,
           'holos': holos,
           'antennas': antennas
           }
    return render_to_response('home/holography.djhtml', ctx, context_instance=RequestContext(request))
