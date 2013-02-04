from django.db import models
from django.conf import settings
# Create your models here.

class Antenna(models.Model):
    """
    Model to the antennas
    """

    name = models.CharField(max_length=5)
    
    # ste configuration fields

    STEs = tuple([tuple([ln, i.strip()]) for ln, i in enumerate(open(settings.CONFIGURATION_DIR+"stes.cfg")) if i.strip()])

    current_ste = models.IntegerField(null=True, choices=STEs)
    requested_ste = models.IntegerField(null=True, blank=True, choices=STEs)

    def __unicode__(self):
        return '%s'%self.name
