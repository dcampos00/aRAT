from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class History(models.Model):
    date_time = models.DateTimeField()
    request = models.TextField()

    def __unicode__(self):
        return "Request: %s"%date_time.strftime("%Y-%m-%d")

class TableHeader(models.Model):
    """
    The header for the tables are stored here, each resource
    can have only one header
    """
    text = models.TextField()
    resource = models.CharField(unique=True, max_length=10)

class Resource(models.Model):
    active = models.BooleanField(default=True, blank=True)    

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    errors = models.TextField(default="[]", blank=True)

    def request_text_info(self):
        """Return a formated string with the information of the requester
        and request date/time information
        """
        if self.is_requested():
            text = "%s %s on %s at %s"%(self.requester.first_name,
                                        self.requester.last_name,
                                        self.request_date.strftime("%Y-%m-%d"),
                                        self.request_date.strftime("%H:%M:%S"))
            return text
        else:
            return None

    def is_requested(self):
        """Return if a resource is in requested status or not"""
        return False

    def is_unassigned(self):
        """Return if a resource will be unassigned or not"""
        return False

    def exist_errors(self):
        return eval(self.errors) != [] or self.global_restriction_errors() != []

    def update_restriction_errors(self):
        return

    def restriction_errors(self):
        errors = {}
        errors['global'] = self.global_restriction_errors()
        errors['local'] = self.local_restriction_errors()

        return errors

    def local_restriction_errors(self):
        """Return a list of the resources that have local restriction 
        errors
        """
        return []

    def global_restriction_errors(self):
        """
        Return a list with numbers that indicate the global restriction
        error that ocurrs, if the list is empty so not exist global
        restriction errors
        """
        return []

    def text_status(self):
        return []

    def html_status(self):
        """Return status in HTML format"""

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
    """Model to the antennas"""

    name = models.CharField(max_length=5, unique=True)

    # ste configuration fields
    STEs = tuple([tuple([i.strip(), i.strip()]) 
                  for i 
                  in open(settings.CONFIGURATION_DIR+'stes.cfg').readlines() 
                  if i.strip()])

    current_ste = models.CharField(max_length=10, null=True, choices=STEs)
    requested_ste = models.CharField(max_length=10, null=True, blank=True, choices=STEs)

    current_band = models.CharField(default="[]", max_length=100)
    requested_band = models.CharField(default="[]", blank=True, max_length=100)

    vendor = models.CharField(null=True, max_length=10)

    def text_status(self):
        text_status = []
        if self.is_requested():
            if self.is_ste_request():
                text = "%s will be changed to %s"%(self, 
                                                   self.requested_ste)
                text_status.append(text)

            if self.is_band_request():
                if self.requested_band == "[-1]":
                    text = "The bands %s will be unassigned of %s."%(self.current_band,
                                                                    self)
                else:
                    text = "The bands %s will be assigned to %s."%(self.requested_band,
                                                                   self)
                text_status.append(text)
        else:
            text = "%s is in %s"%(self, self.current_ste)
            text_status.append(text)

        if self.exist_errors():
            for text in self.text_error():
                text_status.append("Error: %s"%text)

        if self.is_ste_request():
            text_request = "-- Request done by %s"%self.request_text_info()
            text_status.append(text_request)

        return text_status

    def global_restriction_errors(self):
        errors = []
        if (self.requested_ste is None and self.current_ste is None):
            pass
        
        if self.requested_ste is not None:
            ste = self.requested_ste
        else:
            ste = self.current_ste

        if ste == 'VENDOR':
            if self.is_band_request() and self.requested_band != "[-1]":
                errors.append(2)
        else:
            pads = PAD.objects.filter(models.Q(current_antenna=self, assigned=True) | models.Q(requested_antenna=self))
            if pads:
                pass
            else:
                errors.append(1)

            if ste != "TFOHG":
                # Band restrcition
                if self.is_band_request():
                    if self.requested_band == "[]":
                        errors.append(5)
                else:
                    if self.current_band == "[]":
                        errors.append(5)

        return errors

    def text_error(self):
        result = []

        for e in self.global_restriction_errors():
            if e == 1:
                text_error = "The Antenna must have associated a PAD."
            elif e == 2:
                text_error = "The Antenna must have associated a STE."
            elif e == 5:
                text_error = "The Antenna must have associated a bands configuration."
            else:
                continue
            result.append(text_error)

        return result

    def is_ste_request(self):
        return (self.requested_ste != self.current_ste
                       and self.requested_ste is not None)

    def is_band_request(self):
        return (self.requested_band != self.current_band
                and self.requested_band != "[]")

    def is_requested(self):
        return self.is_ste_request() or self.is_band_request()

    def __unicode__(self):
        return '%s'%self.name

class PAD(Resource):
    """Model for the PAD resource"""

    location = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=10, unique=True)
    assigned = models.BooleanField(default=True, blank=True)

    current_antenna = models.ForeignKey(Antenna,
                                           related_name="current_pad_antenna",
                                           null=True,
                                           on_delete=models.SET_NULL)
    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_pad_antenna",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)

    def update_restriction_errors(self, caller=[]):
        """
        This method updates the restriction errors that could have
        a resource
        
        Arguments:
        - `caller`: Is a list of resources that call this method, with this
        information the method will do not call recurvely until the infinite
        """

        pad_to_check = []
        for pad_id in eval(self.errors):
            pad_to_check.append(PAD.objects.get(id=pad_id))

        tmp_errors = []

        local_errors = self.local_restriction_errors()
        new_pad_to_check = [pad for pad in local_errors if pad not in pad_to_check]
        pad_to_check = pad_to_check + new_pad_to_check

        caller.append(self) # the caller list is updated
        for pad in pad_to_check:
            if pad not in caller:
                pad.errors = pad.update_restriction_errors(caller=caller)

        caller.remove(self)

        for pad in local_errors:
            tmp_errors.append(pad.id)

        self.errors = str(tmp_errors)

        self.save()

    def local_restriction_errors(self):
        pad_errors = []
        
        for pad in PAD.objects.all():
            if self != pad:
                if self.requested_antenna is None:
                    if (self.current_antenna == pad.requested_antenna
                        and self.current_antenna is not None):
                        pad_errors.append(pad)
                    elif (self.current_antenna is not None
                          and self.current_antenna == pad.current_antenna
                          and pad.requested_antenna is None
                          and pad.assigned):
                        pad_errors.append(pad)
                else:
                    if self.requested_antenna == pad.requested_antenna:
                        pad_errors.append(pad)
                    elif (self.requested_antenna == pad.current_antenna
                          and pad.requested_antenna is None
                          and pad.assigned):
                        pad_errors.append(pad)

        return pad_errors

    def global_restriction_errors(self):
        if self.requested_antenna is not None:
            antenna = self.requested_antenna
        elif self.is_requested():
            return []
        elif self.current_antenna is not None:
            antenna = self.current_antenna
        else:
            return []

        if antenna.requested_ste is not None:
            ste = antenna.requested_ste
        elif antenna.current_ste is not None:
            ste = antenna.current_ste
        else:
            return [1]

        if self.location == 'AOS' and ste == 'AOS':
            return []
        elif self.location == 'OSF' and (ste == 'TFINT' or ste == 'TFSD' or ste == 'TFOHG'):
            return []
        else:
            return [1]

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.is_requested()):
            if self.assigned == True:
                text = "%s will be changed to %s."%(self.requested_antenna, self)
            else:
                text = "The %s will be unassigned."%(self)
            result.append(text)
        else:
            text = "The %s is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        if self.exist_errors():
            for text in self.text_error():
                result.append("Error: %s"%text)

        if self.is_requested():
            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        error = []

        # the antenna is selected
        if self.requested_antenna is not None:
            antenna = self.requested_antenna
        else:
            antenna = self.current_antenna

        for e in eval(self.errors):
            text = "The Antenna "
            text += "%s"%antenna
            text += " also will be assigned to "
            text += "%s."%PAD.objects.get(id=e)
            error.append(text)


        for e in self.global_restriction_errors():
            if e == 1:
                text = "PAD and Antenna are in different STEs."
            error.append(text)

        return error

    def is_requested(self):
        return (self.requested_antenna is not None) or self.is_unassigned()

    def is_unassigned(self):
        return (self.current_antenna is not None and self.assigned == False)

    def __unicode__(self):
        return 'PAD %s'%self.name

class CorrelatorConfiguration(Resource):

    caimap = models.IntegerField()
    configuration = models.TextField()
    correlator = models.CharField(max_length=10)
    assigned = models.BooleanField(default=True, blank=True)
    header = models.ForeignKey(TableHeader)

    unique_together = ("caimap", "correlator")

    current_antenna = models.ForeignKey(Antenna,
                                        related_name="current_corr_antenna",
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_corr_antenna",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)

    def update_restriction_errors(self, caller=[]):
        """
        This method updates the restriction errors that could have
        a resource
        
        Arguments:
        - `caller`: Is a list of resources that call this method, with this
        information the method will do not call recurvely until the infinite
        """

        corr_conf_to_check = []
        for corr_conf_id in eval(self.errors):
            corr_conf_to_check.append(
                CorrelatorConfiguration.objects.get(id=corr_conf_id))

        tmp_errors = []

        local_errors = self.local_restriction_errors()
        new_corr_conf_to_check = [corr_conf for corr_conf in local_errors if corr_conf not in corr_conf_to_check]
        corr_conf_to_check = corr_conf_to_check + new_corr_conf_to_check

        caller.append(self) # the caller list is updated
        for corr_conf in corr_conf_to_check:
            if corr_conf not in caller:
                corr_conf.errors = corr_conf.update_restriction_errors(caller=caller)

        caller.remove(self)

        for corr_conf in local_errors:
            tmp_errors.append(corr_conf.id)

        self.errors = str(tmp_errors)

        self.save()

    def local_restriction_errors(self):
        configuration_errors = []
        
        for corr_config in CorrelatorConfiguration.objects.all():
            if self != corr_config and corr_config.active:
                if not ((self.correlator == 'BL-Corr'
                         and corr_config.correlator == 'ACA-Corr')
                        or (self.correlator == 'ACA-Corr'
                            and corr_config.correlator == 'BL-Corr')):
                    if self.requested_antenna is None:
                        if (self.current_antenna == corr_config.requested_antenna
                            and self.current_antenna is not None):
                            configuration_errors.append(corr_config)
                        elif (self.current_antenna is not None
                              and self.current_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna is None
                              and corr_config.assigned):
                            configuration_errors.append(corr_config)
                    else:
                        if self.requested_antenna == corr_config.requested_antenna:
                            configuration_errors.append(corr_config)
                        elif (self.requested_antenna == corr_config.current_antenna
                              and corr_config.requested_antenna == None
                              and corr_config.assigned):
                            configuration_errors.append(corr_config)

        return configuration_errors

    def global_restriction_errors(self):
        errors = []
        if self.requested_antenna is not None:
            antenna = self.requested_antenna
        elif self.is_requested():
            return []
        elif self.current_antenna is not None:
            antenna = self.current_antenna
        else:
            return []

        if antenna.requested_ste is not None:
            ste = antenna.requested_ste
        elif antenna.current_ste is not None:
            ste = antenna.current_ste
        else:
            print "%s"%antenna
            errors.append(2)

        pads = PAD.objects.filter(models.Q(current_antenna=antenna, requested_antenna=None) | models.Q(requested_antenna=antenna))

        if pads:
            pass
        else:
            errors.append(3)

        if self.correlator == 'BL-Corr' and (ste == 'AOS'):
            pass
        elif self.correlator == 'ACA-Corr' and (ste == 'AOS'):
            pass
        elif self.correlator == 'OSF-Corr' and (ste == 'TFINT'):
            pass
        elif self.correlator == 'ATF-Corr' and (ste == 'TFSD'):
            pass
        elif ste == 'VENDOR':
            errors.append(2)
        else:
            errors.append(1)

        return errors

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.is_requested()):
            if self.assigned:
                text = "%s will be changed to %s."%(self.requested_antenna, self)
            else:
                text = "The %s Configuration will be unassigned."%(self)
            result.append(text)
        else:
            text = "The %s Configuration is assigned to %s"%(self, self.current_antenna)
            result.append(text)
        
        if self.exist_errors():
            for text in self.text_error():
                result.append("Error: %s"%text)

        if self.is_requested():
            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)

        return result

    def text_error(self):
        """
        Method that returns the Correlator Configuration errors
        in a list when each element of the list corresponds to one error
        """
        error = []
        for e in eval(self.errors):
            text = "The Antenna %s also will be assigned the %s"%(
                self.requested_antenna,
                CorrelatorConfiguration.objects.get(id=e)
                )
            text += " Correlator Configuration."
            error.append(text)


        for e in self.global_restriction_errors():
            if e == 1:
                text = "The Correlator and the Antenna are in different locations."
            elif e == 2:
                text = "The Antenna must be associated to a STE."
            elif e == 3:
                text = "The Antenna must have associated a PAD."
            error.append(text)

        return error

    def is_requested(self):
        return (self.requested_antenna is not None
                or (self.current_antenna is not None and self.assigned == False))

    def drx_data(self):
        if self.correlator == 'ACA-Corr':
            return None, None, None, None
        configuration = eval(self.configuration)
        drxbbpr0 = "%s-%s"%(configuration[-8], configuration[-7]) if configuration[-8] != " " else None
        drxbbpr1 = "%s-%s"%(configuration[-6], configuration[-5]) if configuration[-6] != " " else None
        drxbbpr2 = "%s-%s"%(configuration[-4], configuration[-3]) if configuration[-4] != " " else None
        drxbbpr3 = "%s-%s"%(configuration[-2], configuration[-1]) if configuration[-2] != " " else None
        return drxbbpr0, drxbbpr1, drxbbpr2, drxbbpr3

    def dtsr_data(self):
        if self.correlator != 'ACA-Corr':
            return None, None, None, None
        configuration = eval(self.configuration)
        dtsrbbpr0 = "%s-%s"%(configuration[-8], configuration[-7]) if configuration[-8] != " " else None
        dtsrbbpr1 = "%s-%s"%(configuration[-6], configuration[-5]) if configuration[-6] != " " else None
        dtsrbbpr2 = "%s-%s"%(configuration[-4], configuration[-3]) if configuration[-4] != " " else None
        dtsrbbpr3 = "%s-%s"%(configuration[-2], configuration[-1]) if configuration[-2] != " " else None
        return dtsrbbpr0, dtsrbbpr1, dtsrbbpr2, dtsrbbpr3

    def cai_acacai_data(self):
        if self.correlator != 'ACA-Corr':
            return self.caimap, None
        else:
            return None, self.caimap

    def __unicode__(self):
        return "%s - %s"%(self.caimap,
                               self.configuration)

class CentralloConfiguration(Resource):

    identifier = models.CharField(max_length=20)
    configuration = models.TextField()
    centrallo = models.CharField(max_length=10, blank=True)
    assigned = models.BooleanField(default=True, blank=True)
    header = models.ForeignKey(TableHeader)

    unique_together = (identifier, centrallo)

    current_antenna = models.ForeignKey(Antenna,
                                           related_name="current_clo_antenna",
                                           null=True,
                                           on_delete=models.SET_NULL)
    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_clo_antenna",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)

    def update_restriction_errors(self, caller=[]):
        """
        This method updates the restriction errors that could have
        a resource
        
        Arguments:
        - `caller`: Is a list of resources that call this method, with this
        information the method will do not call recurvely until the infinite
        """

        clo_conf_to_check = []
        for clo_conf_id in eval(self.errors):
            clo_conf_to_check.append(CentralloConfiguration.objects.get(id=clo_conf_id))

        tmp_errors = []

        local_errors = self.local_restriction_errors()
        new_clo_conf_to_check = [clo_conf for clo_conf in local_errors if clo_conf not in clo_conf_to_check]
        clo_conf_to_check = clo_conf_to_check + new_clo_conf_to_check

        caller.append(self) # the caller list is updated
        for clo_conf in clo_conf_to_check:
            if clo_conf not in caller:
                clo_conf.errors = clo_conf.update_restriction_errors(caller=caller)

        caller.remove(self)

        for clo_conf in local_errors:
            tmp_errors.append(clo_conf.id)

        self.errors = str(tmp_errors)

        self.save()

    def local_restriction_errors(self):
        configuration_errors = []
        
        for clo_config in CentralloConfiguration.objects.all():
            if self != clo_config and clo_config.active:
                if self.requested_antenna is None:
                    if (self.current_antenna == clo_config.requested_antenna
                        and self.current_antenna is not None):
                        configuration_errors.append(clo_config)
                    elif (self.current_antenna is not None
                          and self.current_antenna == clo_config.current_antenna
                          and clo_config.requested_antenna is None
                          and clo_config.assigned):
                        configuration_errors.append(clo_config)
                else:
                    if self.requested_antenna == clo_config.requested_antenna:
                        configuration_errors.append(clo_config)
                    elif (self.requested_antenna == clo_config.current_antenna
                          and clo_config.requested_antenna is None
                          and clo_config.assigned):
                        configuration_errors.append(clo_config)

        return configuration_errors

    def global_restriction_errors(self):
        errors = []

        if self.requested_antenna is not None:
            antenna = self.requested_antenna
        elif self.is_requested():
            return []
        elif self.current_antenna is not None:
            antenna = self.current_antenna
        else:
            return []

        if antenna.requested_ste is not None:
            ste = antenna.requested_ste
        elif antenna.current_ste is not None:
            ste = antenna.current_ste
        else:
            errors.append(2)

        pads = PAD.objects.filter(models.Q(current_antenna=antenna, requested_antenna=None) | models.Q(requested_antenna=antenna))

        if pads:
            pass
        else:
            errors.append(3)

        if self.centrallo == 'AOS' and (ste == 'AOS'):
            pass
        elif self.centrallo == 'TFINT' and (ste == 'TFINT'):
            pass
        elif ste == 'VENDOR':
            errors.append(2)
        else:
            errors.append(1)
        
        return errors

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if (self.is_requested()):
            if self.assigned == True:
                text = "%s will be changed to %s CentralLO Configuration."%(self.requested_antenna, self)
            else:
                text = "The %s Configuration will be unassigned."%(self)
            result.append(text)
        else:
            text = "The %s Configuration is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        if self.exist_errors():
            for text in self.text_error():
                result.append("Error: %s"%text)

        if self.is_requested():
            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)


        return result

    def text_error(self):
        """
        Method that returns the CentralLO Configuration restriction
        errors in a list when each element of the list corresponds
        to one error
        """
        error = []
        for e in eval(self.errors):
            text = "The Antenna %s also will be assigned the %s CentralLO Configuration."%(
                self.requested_antenna,
                CentralloConfiguration.objects.get(id=e))
            error.append(text)

        for e in self.global_restriction_errors():
            if e == 1:
                text = "The CentralLO and the Antenna are in different locations."
            elif e == 2:
                text = "The Antenna must be associated to a STE."
            elif e == 3:
                text = "The Antenna must have associated a PAD."
            error.append(text)

        return error

    def is_requested(self):
        return (self.requested_antenna is not None
                or (self.current_antenna is not None and self.assigned == False))

    def sas_ch(self):
        return int(eval(self.configuration)[0])

    def sas_node(self):
        return eval(self.configuration)[1]

    def llc_ch(self):
        return int(eval(self.configuration)[2])

    def llc_node(self):
        return eval(self.configuration)[3]

    def __unicode__(self):
        return "%s - %s"%(self.identifier, self.configuration)

class HolographyConfiguration(Resource):
    """Class that represents the Model of Holography Receptor Configuration"""

    name = models.CharField(max_length=30)
    assigned = models.BooleanField(default=True, blank=True)
    current_antenna = models.ForeignKey(Antenna,
                                           related_name="current_holo_antenna",
                                           null=True,
                                           on_delete=models.SET_NULL)
    requested_antenna = models.ForeignKey(Antenna,
                                          related_name="requested_holo_antenna",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)

    def update_restriction_errors(self, caller=[]):
        """
        This method updates the restriction errors that could have
        a resource
        
        Arguments:
        - `caller`: Is a list of resources that call this method, with this
        information the method will do not call recurvely until the infinite
        """

        holo_to_check = []
        for holo_id in eval(self.errors):
            holo_to_check.append(HolographyConfiguration.objects.get(id=holo_id))

        tmp_errors = []

        local_errors = self.local_restriction_errors()
        new_holo_to_check = [holo for holo in local_errors if holo not in holo_to_check]
        holo_to_check = holo_to_check + new_holo_to_check

        # the caller list is updated
        caller.append(self)
        for holo in holo_to_check:
            if holo not in caller:
                holo.errors = holo.update_restriction_errors(caller=caller)

        caller.remove(self)

        for holo in local_errors:
            tmp_errors.append(holo.id)

        self.errors = str(tmp_errors)

        self.save()

    def local_restriction_errors(self):
        configuration_errors = []
        
        for holo_config in HolographyConfiguration.objects.all():
            if self != holo_config and holo_config.active:
                if self.requested_antenna is None:
                    if (self.current_antenna == holo_config.requested_antenna
                        and self.current_antenna is not None):
                        configuration_errors.append(holo_config)
                    elif (self.current_antenna is not None
                          and self.current_antenna == holo_config.current_antenna
                          and holo_config.requested_antenna is None
                          and holo_config.assigned):
                        configuration_errors.append(holo_config)
                else:
                    if self.requested_antenna == holo_config.requested_antenna:
                        configuration_errors.append(holo_config)
                    elif (self.requested_antenna == holo_config.current_antenna
                          and holo_config.requested_antenna is None
                          and holo_config.assigned):
                        configuration_errors.append(holo_config)

        return configuration_errors

    def global_restriction_errors(self):
        errors = []
        if self.requested_antenna is not None:
            antenna = self.requested_antenna
        elif self.is_requested():
            return []
        elif self.current_antenna is not None:
            antenna = self.current_antenna
        else:
            return []

        if antenna.requested_ste is not None:
            ste = antenna.requested_ste
        elif antenna.current_ste is not None:
            ste = antenna.current_ste
        else:
            errors.append(2)

        pads = PAD.objects.filter(models.Q(current_antenna=antenna, requested_antenna=None) | models.Q(requested_antenna=antenna))

        if pads:
            pass
        else:
            errors.append(3)

        if ste == 'TFOHG':
            pass
        else:
            errors.append(1)

        return errors

    def text_status(self):
        """
        This method returns a list that describe the current status of the
        resource
        """
        result = []
        text = None
        if self.is_requested():
            if self.assigned == True:
                text = "%s will be assigned to %s."%(self, self.requested_antenna)
            else:
                text = "The %s will be unassigned."%(self)
            result.append(text)
        else:
            text = "The %s is assigned to %s"%(self, self.current_antenna)
            result.append(text)

        if self.exist_errors():
            for text in self.text_error():
                result.append("Error: %s"%text)

        if self.is_requested():
            text_request = "-- Request done by %s"%self.request_text_info()
            result.append(text_request)

        return result

    def text_error(self):
        """
        Method that returns the pad errors in a list when each element of the list
        correspond to one error
        """
        if self.is_requested():
            antenna = self.requested_antenna
        else:
            antenna = self.current_antenna

        error = []
        for e in eval(self.errors):
            text = "The Antenna %s also will have assigned %s."%(antenna,
                                                                 HolographyConfiguration.objects.get(id=e))
            error.append(text)

        for e in self.global_restriction_errors():
            if e == 1:
                text = "The Antenna %s is not in TFOHG."%antenna
            elif e == 2:
                text = "The Antenna must be associated to a STE."
            elif e == 3:
                text = "The Antenna must have associated a PAD."
            error.append(text)

        return error

    def is_requested(self):
        return (self.requested_antenna is not None
                or (self.current_antenna is not None and self.assigned == False))

    def __unicode__(self):
        return "Holography Receptor %s"%self.name
