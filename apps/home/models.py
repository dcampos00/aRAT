from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Antenna(models.Model):
    """
    Model to the antennas
    """

    name = models.CharField(max_length=5)
    active = models.BooleanField(default=True, blank=True)    

    # ste configuration fields
    STEs = tuple([tuple([ln, i.strip()]) for ln, i in enumerate(open(settings.CONFIGURATION_DIR+'stes.cfg')) if i.strip()])

    current_ste = models.IntegerField(null=True, choices=STEs)
    requested_ste = models.IntegerField(null=True, blank=True, choices=STEs)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '%s'%self.name

class PAD(models.Model):
    _LINES = []
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'pads.cfg')):
        line_string = line_string.strip()
        if line_string:
            _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)
    location = models.TextField(blank=True)
    assigned = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    current_antenna = models.OneToOneField(Antenna, related_name="current_pad_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_pad_antenna", null=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def restriction_errors(self):
        errors = {}
        errors['local'] = self.local_restriction_errors()
        errors['global'] = self.global_restriction_errors()
        return errors

    def local_restriction_errors(self):
        pad_errors = []
        for pad in PAD.objects.all():
            if self != pad:
                if self.requested_antenna == None:
                    if self.current_antenna == pad.requested_antenna and self.current_antenna != None:
                        pad_errors.append(pad.name())
                    elif self.current_antenna == pad.current_antenna and pad.requested_antenna == None and pad.assigned == True:
                        pad_errors.append(pad.name())
                else:
                    if self.requested_antenna == pad.requested_antenna:
                        pad_errors.append(pad.name())
                    elif self.requested_antenna == pad.current_antenna and pad.requested_antenna == None and pad.assigned == True:
                        pad_errors.append(pad.name())

        if pad_errors == []:
            pad_errors = None
        return pad_errors

    def global_restriction_errors(self):
        if self.requested_antenna != None:
            antenna = self.requested_antenna
        elif self.current_antenna != None:
            antenna = self.current_antenna
        else:
            return False

        if antenna.requested_ste != None:
            ste = antenna.get_requested_ste_display()
        elif antenna.current_ste != None:
            ste = antenna.get_current_ste_display()
        else:
            return True

        if self.location == 'AOS' and (ste == 'AOS' or ste == 'AOS2'):
            return False
        elif self.location == 'OSF' and (ste == 'TFINT' or ste == 'TFSD' or ste == 'TFOHG'):
            return False
        else:
            return True

    def name(self):
        return self.get_line_display().split()[0]

    def save(self):
        self.location = self.get_line_display().split()[1]
        super(PAD, self).save()

    def __unicode__(self):
        return 'PAD %s'%self.name()

class CentralLO(models.Model):
    # in the db is saved the line of the configuration file that match with the configuration of
    # the CentralLO
    LINES = []
    for line_number, line in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg')):
        line.strip()
        if line:
            line = line.strip().split()[0:-1]
            LINES.append((line_number, str(line)[2:-2].replace("', '"," ")))

    LINES = tuple(LINES)

    line = models.IntegerField(choices=LINES, unique=True)
    assigned = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    current_antenna = models.OneToOneField(Antenna, related_name="current_clo_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_clo_antenna", null=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s"%(self.get_line_display())

class CorrelatorConfiguration(models.Model):
    # in the db is saved the line of the configuration file that match with the configuration of
    # the CentralLO
    _LINES = []
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
        if line_string[0] != "#":
            line_string = line_string.strip()
            if line_string:
                _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)

    # this is a calculated field from line display value
    correlator = models.TextField(blank=True)
    assigned = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)

    current_antenna = models.ForeignKey(Antenna, related_name="current_corr_antenna", null=True, blank=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_corr_antenna", null=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def restriction_errors(self):
        errors = {}
        errors['local'] = self.local_restriction_errors()
        errors['global'] = self.global_restriction_errors()
        return errors

    def local_restriction_errors(self):
        configuration_errors = []
        
        for corr_config in CorrelatorConfiguration.objects.all():
            if self != corr_config and corr_config.active:
                if not ((self.correlator == 'BL-Corr' and corr_config.correlator == 'ACA-Corr')
                        or (self.correlator == 'ACA-Corr' and corr_config.correlator == 'BL-Corr')):
                    if self.requested_antenna == None:
                        if (self.current_antenna == corr_config.requested_antenna
                            and self.current_antenna != None):
                            configuration_errors.append(corr_config.configuration())
                        elif (self.current_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna == None
                              and corr_config.assigned == True):
                            configuration_errors.append(corr_config.configuration())
                    else:
                        if self.requested_antenna == corr_config.requested_antenna:
                            configuration_errors.append(corr_config.configuration())
                        elif (self.requested_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna == None
                              and corr_config.assigned == True):
                            configuration_errors.append(corr_config.configuration())

        if configuration_errors == []:
            configuration_errors = None

        return configuration_errors

    def global_restriction_errors(self):
        if self.requested_antenna != None:
            antenna = self.requested_antenna
        elif self.current_antenna != None:
            antenna = self.current_antenna
        else:
            return False

        if antenna.requested_ste != None:
            ste = antenna.get_requested_ste_display()
        elif antenna.current_ste != None:
            ste = antenna.get_current_ste_display()
        else:
            return True

        if self.correlator == 'BL-Corr' and (ste == 'AOS'):
            return False
        elif self.correlator == 'ACA-Corr' and (ste == 'AOS' or ste == 'AOS2'):
            return False
        elif self.correlator == 'OSF-Corr' and (ste == 'TFINT'):
            return False
        elif self.correlator == 'ATF-Corr' and (ste == 'TFSD'):
            return False
        else:
            return True

    def line_number(self):
        return "%d"%self.line

    def configuration(self):
        configuration = str(self.get_line_display().split()[0:-1]).replace("', u'", ' ')[3:-2]
        return "%s"%configuration

    def caimap(self):
        caimap = self.get_line_display().split()[0]
        return "%s"%caimap

    def save(self):
        self.correlator = self.get_line_display().split()[-1]
        super(CorrelatorConfiguration, self).save()

    def __unicode__(self):
        return "Line %s - %s [%s]"%(self.line, self.configuration(), self.correlator)
