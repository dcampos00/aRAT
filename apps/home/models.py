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

    current_antenna = models.OneToOneField(Antenna, related_name="Current Antenna", null=True)
    requested_antenna = models.ForeignKey(Antenna, related_name="Requested Antenna", null=True, blank=True)

    requester = models.ForeignKey(User, null=True, blank=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return 'PAD %s'%self.name
