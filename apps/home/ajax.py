from datetime import datetime
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

# are imported the models of the application
from aRAT.apps.home.models import (Antenna, PAD,
                                   CorrelatorConfiguration,
                                   CentralloConfiguration,
                                   HolographyConfiguration)
from aRAT.apps.common.models import Configuration

from aRAT.apps.home.views import read_only as check_read_only
from django.conf import settings


@dajaxice_register
def ste_update_alerts(request, ste_id='', antenna_id=''):
    """
    allows keep update the requests status for STEs configuration.

    If ste_id and antenna_id is *None* the functions returns the current
    status of the all ste configuration.

    If antenna_id is different to *None* the antenna is updated.

    Arguments:
    - `ste_id`: is the id of STE that will be assigned to the Antenna
    (in the application the STE_id is its *name*)
    - `antenna_id`: the id of the Antenna that will be updated
    """

    dajax = Dajax()  # object that manage the AJAX connection

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    # first the antenna information is updated
    # if is passed a antenna_id and the application is not in read_only mode
    # the information of the Antenna is update
    if antenna_id != '' and not read_only:
        antenna = Antenna.objects.get(id=antenna_id)
        # if the ste_id is passed and if the ste is not the same that
        # the current a new STE is assigned to the antenna
        if ste_id != '' and ste_id != antenna.current_ste:
            antenna.requested_ste = ste_id
        else:
            antenna.requested_ste = None

        # The requester and request_date is updated
        antenna.requester = request.user
        antenna.request_date = datetime.now()
        antenna.save()  # the Antenna is saved

    # is loaded all current status of the ste configuration
    antennas = Antenna.objects.all()
    for antenna in antennas:
        if not antenna.active:
            continue

        # the status of the antenna is obtained in HTML format
        status = antenna.html_status()

        # the data is passed to the template function update_status
        dajax.add_data({'antenna': antenna.id,
                        'requested_ste': antenna.requested_ste,
                        'current_ste': antenna.current_ste,
                        'is_requested': antenna.is_requested(),
                        'error': antenna.exist_errors(),
                        'read_only': read_only,
                        'status': status},
                       'update_status')

    return dajax.json()


@dajaxice_register
def band_update_alerts(request, band_array=[], antenna_id=''):
    """
    Return the status bands assigned to the antennas.

    If antenna_id is not *None* the antenna's bands of the antenna
    with id equal to antenna_id are updated with band_array

    Arguments:
    `band_array`: array that contains the bands that will be assigned
    to the antenna
    `antenna_id`: id of the antenna that will be updated
    """

    dajax = Dajax()  # object that manage the AJAX response

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    if antenna_id != '' and not read_only:
        antenna = Antenna.objects.get(id=antenna_id)
        # if the ste_id is passed and if the ste is not the same that
        # the current a new STE is assigned to the antenna
        if band_array and str(band_array) != antenna.current_band:
            antenna.requested_band = str(band_array)
        else:
            antenna.requested_band = "[]"

        # The requester and request_date is updated
        # antenna.requester = request.user
        # antenna.request_date = datetime.now()
        antenna.save()  # the Antenna is saved

    for antenna in Antenna.objects.all():
        # if a antenna is not active is skipped
        if not antenna.active:
            continue

        # the status of the antenna is obtained in HTML format
        status = antenna.html_status()

        requested_band = antenna.requested_band
        if requested_band == "[-1]":
            requested_band = "[]"

        # the data is passed to the template function update_status
        dajax.add_data({'antenna': antenna.id,
                        'requested_band': requested_band,
                        'current_band': antenna.current_band,
                        'is_requested': antenna.is_requested(),
                        'error': antenna.exist_errors(),
                        'read_only': read_only,
                        'status': status},
                       'update_status')

    return dajax.json()


@dajaxice_register
def pad_update_alerts(request, pad_id='', antenna_id=''):
    """
    Allows keep update the alerts for PADs. Also update the configuration
    of the PAD

    If pad_id is not *None* the antenna assigned to the PAD is updated
    to the antenna with the id equal to antenna_id

    Arguments:
    - `pad_id`: id value of a pad that will be updated
    - `antenna_id`: id value of an antenna that will be assigned to a pad
    """

    dajax = Dajax()

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    # first the pad information is updated
    if pad_id != '' and not read_only:
        pad = PAD.objects.get(id=pad_id)
        # this happend when a PAD will be unassigned
        if antenna_id == 'None' and pad.current_antenna is not None:
            pad.assigned = False
            pad.requested_antenna = None
        # if a PAD will be changed to another antenna
        elif (antenna_id != ''
              and antenna_id != 'None'
              and pad.current_antenna != Antenna.objects.get(id=antenna_id)):
            pad.requested_antenna = Antenna.objects.get(id=antenna_id)
            pad.assigned = True
        # if a request is deleted
        else:
            pad.requested_antenna = None
            pad.assigned = True
        pad.requester = request.user
        pad.request_date = datetime.now()
        pad.save()  # the PAD information is saved
        pad.update_restriction_errors()  # the restriction errors are updated

    # are loaded all current status of the PADs
    for pad in PAD.objects.all():
        if not pad.active:
            continue

        current_antenna_name = current_antenna_id = None
        requested_antenna_name = requested_antenna_id = None

        if pad.current_antenna is not None:
            current_antenna_name = pad.current_antenna.name
            current_antenna_id = pad.current_antenna.id
        if pad.requested_antenna is not None:
            requested_antenna_name = pad.requested_antenna.name
            requested_antenna_id = pad.requested_antenna.id

        status = pad.html_status()
        exist_errors = pad.exist_errors()

        dajax.add_data({'resource': {'id': pad.id,
                                     'name': pad.name,
                                     'assigned': pad.assigned,
                                     'type': 'pad'},
                        'current_antenna': {'id': current_antenna_id,
                                            'name': current_antenna_name},
                        'requested_antenna': {'id': requested_antenna_id,
                                              'name': requested_antenna_name},
                        'status': status,
                        'error': exist_errors,
                        'is_requested': pad.is_requested(),
                        'read_only': read_only
                        },
                       'update_status')

    return dajax.json()


@dajaxice_register
def corr_update_alerts(request, configuration_id='', antenna_id=''):
    """
    Keeps updated the alerts of Correlator Configuration

    If configuration_id is not *None* then the configuration with id equal
    to configuration_id assigned to the antenna with id equal to antenna_id

    Arguments:
    `configuration_id`: identifier of the correlator configuration
    `antenna_id`: identifier of the Antenna to be requested
    """
    dajax = Dajax()

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    # first the correlator configuration is updated
    if configuration_id != '' and not read_only:
        corr = CorrelatorConfiguration.objects.get(id=configuration_id)
        if antenna_id == 'None' and corr.current_antenna is not None:
            corr.assigned = False
            corr.requested_antenna = None
        elif (antenna_id != ''
              and antenna_id != 'None'
              and corr.current_antenna != Antenna.objects.get(id=antenna_id)):
            corr.requested_antenna = Antenna.objects.get(id=antenna_id)
            corr.assigned = True
        else:
            corr.requested_antenna = None
            corr.assigned = True
        corr.requester = request.user
        corr.request_date = datetime.now()
        corr.save()
        corr.update_restriction_errors()

    # is loaded all current status of the correlator configurations
    for corr in CorrelatorConfiguration.objects.all():
        if not corr.active:
            continue

        # the antenna values are set to None to avoid errors
        # if current_antenna and requested_antenna are not object
        current_antenna_name = current_antenna_id = None
        requested_antenna_name = requested_antenna_id = None

        if corr.current_antenna is not None:
            current_antenna_name = corr.current_antenna.name
            current_antenna_id = corr.current_antenna.id
        if corr.requested_antenna is not None:
            requested_antenna_name = corr.requested_antenna.name
            requested_antenna_id = corr.requested_antenna.id

        status = corr.html_status()
        exist_errors = corr.exist_errors()

        dajax.add_data({'resource': {'id': corr.id,
                                     'name': corr.configuration,
                                     'assigned': corr.assigned,
                                     'type': 'corr'},
                        'current_antenna': {'id': current_antenna_id,
                                            'name': current_antenna_name},
                        'requested_antenna': {'id': requested_antenna_id,
                                              'name': requested_antenna_name},
                        'status': status,
                        'is_requested': corr.is_requested(),
                        'error': exist_errors,
                        'read_only': read_only
                        },
                       'update_status')

    return dajax.json()


@dajaxice_register
def clo_update_alerts(request, configuration_id='', antenna_id=''):
    """
    Keeps updated the alerts of CentralLO Configuration.

    If configuration_id is not *None* then the configuration with id equal
    to configuration_id assigned to the antenna with id equal to antenna_id

    Arguments:
    `configuration_id`: identifier of the centrallo configuration.
    `antenna_id`: identifier of the Antenna to be requested.
    """

    dajax = Dajax()

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    # first the clo conf information is updated
    if configuration_id != '' and not read_only:
        clo = CentralloConfiguration.objects.get(id=configuration_id)
        if antenna_id == 'None' and clo.current_antenna is not None:
            clo.assigned = False
            clo.requested_antenna = None
        elif (antenna_id != ''
              and antenna_id != 'None'
              and clo.current_antenna != Antenna.objects.get(id=antenna_id)):
            clo.requested_antenna = Antenna.objects.get(id=antenna_id)
            clo.assigned = True
        else:
            clo.requested_antenna = None
            clo.assigned = True
        clo.requester = request.user
        clo.request_date = datetime.now()
        clo.save()
        clo.update_restriction_errors()

    # are loaded all current status of the centrallo configurations
    for clo in CentralloConfiguration.objects.all():
        if not clo.active:
            continue

        # the antenna values are set to None to avoid errors
        # if current_antenna and requested_antenna are not object
        current_antenna_name = current_antenna_id = None
        requested_antenna_name = requested_antenna_id = None

        if clo.current_antenna:
            current_antenna_name = clo.current_antenna.name
            current_antenna_id = clo.current_antenna.id
        if clo.requested_antenna:
            requested_antenna_name = clo.requested_antenna.name
            requested_antenna_id = clo.requested_antenna.id

        status = clo.html_status()
        exist_errors = clo.exist_errors()

        dajax.add_data({'resource': {'id': clo.id,
                                     'name': clo.configuration,
                                     'assigned': clo.assigned,
                                     'type': 'clo'},
                        'current_antenna': {'id': current_antenna_id,
                                            'name': current_antenna_name},
                        'requested_antenna': {'id': requested_antenna_id,
                                              'name': requested_antenna_name},
                        'status': status,
                        'is_requested': clo.is_requested(),
                        'read_only': read_only,
                        'error': exist_errors
                        },
                       'update_status')

    return dajax.json()


@dajaxice_register
def holo_update_alerts(request, holo_id='', antenna_id=''):
    """
    Function that keeps updated the alerts of Holography Configuration

    If configuration_id is not *None* then the configuration with id equal
    to configuration_id assigned to the antenna with id equal to antenna_id

    Arguments:
    `holo_id`: identifier of the holography configuration.
    `antenna_id`: identifier of the Antenna to be requested
    """
    dajax = Dajax()

    # is retrieved the current block status of the application
    read_only = check_read_only(request)

    # first the holography configuration information is updated
    if holo_id != '' and not read_only:
        holo = HolographyConfiguration.objects.get(id=holo_id)
        if antenna_id == 'None' and holo.current_antenna is not None:
            holo.assigned = False
            holo.requested_antenna = None
        elif (antenna_id != ''
              and antenna_id != 'None'
              and holo.current_antenna != Antenna.objects.get(id=antenna_id)):
            holo.requested_antenna = Antenna.objects.get(id=antenna_id)
            holo.assigned = True
        else:
            holo.requested_antenna = None
            holo.assigned = True
        holo.requester = request.user
        holo.request_date = datetime.now()
        holo.save()

    # are loaded all current status of the holography configurations
    for holo in HolographyConfiguration.objects.all():
        if not holo.active:
            continue

        # the antenna values are set to None to avoid errors
        # if current_antenna and requested_antenna are not object
        current_antenna_name = current_antenna_id = None
        requested_antenna_name = requested_antenna_id = None

        if holo.current_antenna:
            current_antenna_name = holo.current_antenna.name
            current_antenna_id = holo.current_antenna.id
        if holo.requested_antenna:
            requested_antenna_name = holo.requested_antenna.name
            requested_antenna_id = holo.requested_antenna.id

        status = holo.html_status()
        exist_errors = holo.exist_errors()

        dajax.add_data({'resource': {'id': holo.id,
                                     'name': holo.name,
                                     'assigned': holo.assigned,
                                     'type': 'holo'},
                        'current_antenna': {'id': current_antenna_id,
                                            'name': current_antenna_name},
                        'requested_antenna': {'id': requested_antenna_id,
                                              'name': requested_antenna_name},
                        'status': status,
                        'is_requested': holo.is_requested(),
                        'read_only': read_only,
                        'error': exist_errors
                        },
                       'update_status')

    return dajax.json()
