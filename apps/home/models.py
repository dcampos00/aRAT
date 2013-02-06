from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Antenna(models.Model):
    """
    Model to the antennas
    """

    name = models.CharField(max_length=5)
    
    # ste configuration fields
    STEs = tuple([tuple([ln, i.strip()]) for ln, i in enumerate(open(settings.CONFIGURATION_DIR+'stes.cfg')) if i.strip()])

    current_ste = models.IntegerField(null=True, choices=STEs)
    requested_ste = models.IntegerField(null=True, blank=True, choices=STEs)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '%s'%self.name

class PAD(models.Model):
    name = models.CharField(max_length=5, unique=True)

    current_antenna = models.OneToOneField(Antenna, related_name="current_pad_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_pad_antenna", null=True, blank=True)

    assigned = models.BooleanField(default=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return 'PAD %s'%self.name

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
#    LINES = tuple([tuple([line_number, line.split()[0:-1]]) for line_number, line in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg'))])
    line = models.IntegerField(choices=LINES, unique=True)

    current_antenna = models.OneToOneField(Antenna, related_name="current_clo_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_clo_antenna", null=True, blank=True)

    assigned = models.BooleanField(default=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s"%(self.get_line_display())

class Correlator(models.Model):
    # in the db is saved the line of the configuration file that match with the configuration of
    # the CentralLO
    LINES = []
    for line_number, line in enumerate(open(settings.CONFIGURATION_DIR+'corr.cfg')):
        line.strip()
        if line:
            line = line.strip().split()[0:-1]
            LINES.append((line_number, str(line)[2:-2].replace("', '"," ")))

    LINES = tuple(LINES)
#    LINES = tuple([tuple([line_number, line.split()[0:-1]]) for line_number, line in enumerate(open(settings.CONFIGURATION_DIR+'clo.cfg'))])
    line = models.IntegerField(choices=LINES, unique=True)

    current_antenna = models.ForeignKey(Antenna, related_name="current_corr_antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="requested_corr_antenna", null=True, blank=True)

    assigned = models.BooleanField(default=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s"%(self.get_line_display())
