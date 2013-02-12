from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Resource(models.Model):
    active = models.BooleanField(default=True, blank=True)    

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def request_text_info(self):
        text = "%s %s on %s at %s"%(self.requester.first_name,
                                    self.requester.last_name,
                                    self.request_date.strftime("%Y-%m-%d"),
                                    self.request_date.strftime("%H:%M:%S"))
        return text

    def exist_errors(self):
        if (self.local_restriction_errors() != [] 
            or self.global_restriction_errors()):
            return True
        else:
            return False

    def restriction_errors(self):
        errors = {}
        errors['local'] = self.local_restriction_errors()
        errors['global'] = self.global_restriction_errors()
        return errors

    def local_restriction_errors(self):
        return []

    def global_restriction_errors(self):
        return False

    def text_status(self):
        return []

    def html_status(self):
        """
        This method returns html formated status
        """

        html = ""
        first = True
        for text in self.text_status():
            text = text.replace('Error','<strong>Error</strong>')
            if first:
                html += text
                first = False
            else:
                html += "<br>%s"%text

        return html

class Antenna(Resource):
    """
    Model to the antennas
    """

    name = models.CharField(max_length=5)

    # ste configuration fields
    STEs = tuple([tuple([ln, i.strip()]) 
                  for ln, i 
                  in enumerate(open(settings.CONFIGURATION_DIR+'stes.cfg')) 
                  if i.strip()])

    current_ste = models.IntegerField(null=True, choices=STEs)
    requested_ste = models.IntegerField(null=True, blank=True, choices=STEs)

    def text_status(self):
        text_status = []
        if self.requested_ste != None:
            text = "%s will be changed to %s"%(self, 
                                               self.get_requested_ste_display())
            text_request = "-- Request done by %s"%self.request_text_info()

            text_status.append(text)
            text_status.append(text_request)
        else:
            text = "%s is in %s"%(self, self.get_current_ste_display())
            text_status.append(text)
        return text_status

    def __unicode__(self):
        return '%s'%self.name

class PAD(Resource):
    _LINES = []
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'pads.cfg')):
        line_string = line_string.strip()
        if line_string:
            _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)
    location = models.CharField(max_length=10, blank=True)
    assigned = models.BooleanField(default=True, blank=True)

    current_antenna = models.OneToOneField(Antenna,
                                           related_name="current_pad_antenna",
                                           null=True)
    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_pad_antenna",
                                          null=True, blank=True)

    def local_restriction_errors(self):
        pad_errors = []
        for pad in PAD.objects.all():
            if self != pad:
                if self.requested_antenna == None:
                    if self.current_antenna == pad.requested_antenna and self.current_antenna != None:
                        pad_errors.append(pad)
                    elif self.current_antenna == pad.current_antenna and pad.requested_antenna == None and pad.assigned == True:
                        pad_errors.append(pad)
                else:
                    if self.requested_antenna == pad.requested_antenna:
                        pad_errors.append(pad)
                    elif self.requested_antenna == pad.current_antenna and pad.requested_antenna == None and pad.assigned == True:
                        pad_errors.append(pad)

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

    def line_number(self):
        return self.line

    def save(self):
        self.location = self.get_line_display().split()[1]
        super(PAD, self).save()

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.requested_antenna != None 
            or (self.current_antenna != None and self.assigned == False)):
            if self.assigned == True:
                text = "%s will be changed to %s."%(self.requested_antenna, self)
            else:
                text = "The %s will be unassigned."%(self)
            result.append(text)

            for text in self.text_error():
                result.append("Error: %s"%text)

            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)
        else:
            text = "The %s is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        error = []
        for e in self.local_restriction_errors():
            text = "The Antenna "
            text += self.requested_antenna.__unicode__()
            text += " also will be assigned to "
            text += e.__unicode__()+"."
            error.append(text)


        if self.global_restriction_errors():
            text = "PAD and Antenna are in different STEs."
            error.append(text)

        return error

    def __unicode__(self):
        return 'PAD %s'%self.name()

class CorrelatorConfiguration(Resource):
    # in the db is saved the line of the configuration file that match with the configuration of
    # the CorrelatorConfiguration
    _LINES = []
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
        if line_string[0] != "#":
            line_string = line_string.strip()
            if line_string:
                _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)

    # this is a calculated field from line display value
    correlator = models.CharField(max_length=10, blank=True)
    assigned = models.BooleanField(default=True, blank=True)

    current_antenna = models.ForeignKey(Antenna, related_name="current_corr_antenna", null=True, blank=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_corr_antenna", null=True, blank=True)

    def local_restriction_errors(self):
        configuration_errors = []
        
        for corr_config in CorrelatorConfiguration.objects.all():
            if self != corr_config and corr_config.active:
                if not ((self.correlator == 'BL-Corr' and corr_config.correlator == 'ACA-Corr')
                        or (self.correlator == 'ACA-Corr' and corr_config.correlator == 'BL-Corr')):
                    if self.requested_antenna == None:
                        if (self.current_antenna == corr_config.requested_antenna
                            and self.current_antenna != None):
                            configuration_errors.append(corr_config)
                        elif (self.current_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna == None
                              and corr_config.assigned == True):
                            configuration_errors.append(corr_config)
                    else:
                        if self.requested_antenna == corr_config.requested_antenna:
                            configuration_errors.append(corr_config)
                        elif (self.requested_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna == None
                              and corr_config.assigned == True):
                            configuration_errors.append(corr_config)

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

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.requested_antenna != None 
            or (self.current_antenna != None and self.assigned == False)):
            if self.assigned == True:
                text = "%s will be changed to %s Correlator Configuration."%(self.requested_antenna, self.configuration())
            else:
                text = "The %s Configuration will be unassigned."%(self.configuration())
            result.append(text)

            for text in self.text_error():
                result.append("Error: %s"%text)

            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)
        else:
            text = "The %s Configuration is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        error = []
        for e in self.local_restriction_errors():
            text = "The Antenna %s also will be assigned the %s Correlator Configuration."%(self.requested_antenna, e.configuration())
            error.append(text)


        if self.global_restriction_errors():
            text = "The Correlator and the Antenna are in different locations."
            error.append(text)

        return error

    def __unicode__(self):
        return "Line %s - %s [%s]"%(self.line, self.configuration(), self.correlator)

class CentralloConfiguration(Resource):
    # in the db is saved the line of the configuration file that match with the configuration of
    # the CentralLO
    _LINES = []
    for line_number, line_string in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg')):
        if line_string[0] != "#":
            line_string = line_string.strip()
            if line_string:
                _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)

    #calculated field
    centrallo = models.CharField(max_length=10, blank=True)
    assigned = models.BooleanField(default=True, blank=True)

    current_antenna = models.OneToOneField(Antenna, related_name="current_clo_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_clo_antenna", null=True, blank=True)

    def restriction_errors(self):
        errors = {}
        errors['local'] = self.local_restriction_errors()
        errors['global'] = self.global_restriction_errors()
        return errors

    def local_restriction_errors(self):
        configuration_errors = []
        
        for clo_config in CentralloConfiguration.objects.all():
            if self != clo_config and clo_config.active:
                if self.requested_antenna == None:
                    if (self.current_antenna == clo_config.requested_antenna
                        and self.current_antenna != None):
                        configuration_errors.append(clo_config)
                    elif (self.current_antenna == clo_config.current_antenna
                          and clo_config.requested_antenna == None
                          and clo_config.assigned == True):
                        configuration_errors.append(clo_config)
                else:
                    if self.requested_antenna == clo_config.requested_antenna:
                        configuration_errors.append(clo_config)
                    elif (self.requested_antenna == clo_config.current_antenna
                          and clo_config.requested_antenna == None
                          and clo_config.assigned == True):
                        configuration_errors.append(clo_config)

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

        if self.centrallo == 'AOS' and (ste == 'AOS' or ste == 'AOS2'):
            return False
        elif self.centrallo == 'TFINT' and (ste == 'TFINT'):
            return False
        else:
            return True

    def line_number(self):
        return "%d"%self.line

    def configuration(self):
        configuration = str(self.get_line_display().split()[0:-1]).replace("', u'", ' ')[3:-2]
        return "%s"%configuration

    def save(self):
        self.centrallo = self.get_line_display().split()[-1]
        super(CentralloConfiguration, self).save()

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.requested_antenna != None 
            or (self.current_antenna != None and self.assigned == False)):
            if self.assigned == True:
                text = "%s will be changed to %s CentralLO Configuration."%(self.requested_antenna, self.configuration())
            else:
                text = "The %s Configuration will be unassigned."%(self.configuration())
            result.append(text)

            for text in self.text_error():
                result.append("Error: %s"%text)

            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)
        else:
            text = "The %s Configuration is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        error = []
        for e in self.local_restriction_errors():
            text = "The Antenna %s also will be assigned the %s CentralLO Configuration."%(self.requested_antenna, e.configuration())
            error.append(text)


        if self.global_restriction_errors():
            text = "The CentralLO and the Antenna are in different locations."
            error.append(text)

        return error

    def __unicode__(self):
        return "Line %s - %s [%s]"%(self.line, self.configuration(), self.centrallo)

class HolographyConfiguration(Resource):
    _LINES = []
    for line_number, line_string in enumerate(
        open(settings.CONFIGURATION_DIR+'holography.cfg')):
        if line_string[0] != "#":
            line_string = line_string.strip()
            if line_string:
                _LINES.append((line_number, line_string))

    _LINES = tuple(_LINES)

    line = models.IntegerField(choices=_LINES, unique=True)

    assigned = models.BooleanField(default=True, blank=True)
    current_antenna = models.OneToOneField(Antenna,
                                           related_name="current_holo_antenna",
                                           null=True)
    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_holo_antenna",
                                          null=True,
                                          blank=True)

    def restriction_errors(self):
        errors = {}
        errors['local'] = self.local_restriction_errors()
        errors['global'] = self.global_restriction_errors()
        return errors

    def local_restriction_errors(self):
        configuration_errors = []
        
        for holo_config in HolographyConfiguration.objects.all():
            if self != holo_config and holo_config.active:
                if self.requested_antenna == None:
                    if (self.current_antenna == holo_config.requested_antenna
                        and self.current_antenna != None):
                        configuration_errors.append(holo_config)
                    elif (self.current_antenna == holo_config.current_antenna
                          and holo_config.requested_antenna == None
                          and holo_config.assigned == True):
                        configuration_errors.append(holo_config)
                else:
                    if self.requested_antenna == holo_config.requested_antenna:
                        configuration_errors.append(holo_config)
                    elif (self.requested_antenna == holo_config.current_antenna
                          and holo_config.requested_antenna == None
                          and holo_config.assigned == True):
                        configuration_errors.append(holo_config)

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

        if ste == 'TFOHG':
            return False
        else:
            return True

    def name(self):
        return "%s"%self.get_line_display()

    def line_number(self):
        return "%d"%self.line


    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.requested_antenna != None 
            or (self.current_antenna != None and self.assigned == False)):
            if self.assigned == True:
                text = "%s will be assigned to %s."%(self, self.requested_antenna)
            else:
                text = "The %s will be unassigned."%(self)
            result.append(text)

            for text in self.text_error():
                result.append("Error: %s"%text)

            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)
        else:
            text = "The %s is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        error = []
        for e in self.local_restriction_errors():
            text = "The Antenna %s also will have assigned %s."%(self.requested_antenna, e)
            error.append(text)


        if self.global_restriction_errors():
            text = "The Antenna %s is not in TFOHG."%(self.requested_antenna)
            error.append(text)

        return error

    def __unicode__(self):
        return "Holography Receptor %s"%self.get_line_display()
