from django.db import models

# Create your models here.

class STE(models.Model):
    name = models.CharField(max_length=6, unique=True)
    def __unicode__(self):
        return '%s'%self.name

class DRX(models.Model):
    CHANNELS = (
        (0, 'Channel 0'),
        (1, 'Channel 1'),
        (2, 'Channel 2'),
        (3, 'Channel 3'),
        )
    
    name = models.CharField(max_length=5)
    channel = models.IntegerField(max_length=1, choices=CHANNELS)
    ste = models.ForeignKey(STE, null=True, blank=True)

    def __unicode__(self):
        return 'DRX %s-%s'%(self.channel, self.name)

class DTSR(models.Model):
    CHANNELS = (
        (0, 'Channel 0'),
        (1, 'Channel 1'),
        (2, 'Channel 2'),
        (3, 'Channel 3'),
        )
    
    name = models.CharField(max_length=5)
    channel = models.IntegerField(max_length=1, choices=CHANNELS)
    ste = models.ForeignKey(STE, null=True, blank=True)

    def __unicode__(self):
        return 'DTSR %s-%s'%(self.channel, self.name)

class Antenna(models.Model):
    """
    Model of antennas
    """

    # possibles values to caimaps in base line correlator and aca correlator
    BL_CAIMAPS = tuple([tuple([i, 'CAIMAP %s'%i]) for i in xrange(-1,64)])
    ACA_CAIMAPS = tuple([tuple([i, 'CAIMAP %s'%i]) for i in xrange(-1,16)])

    name = models.CharField(max_length=5)
    
    # ste configuration fields
    current_ste = models.ForeignKey(STE, related_name='current_location', null=True, blank=True)
    requested_ste = models.ForeignKey(STE, related_name='requested_location', null=True, blank=True)

    # baseline caimap fields
    current_bl_caimap = models.IntegerField(null=True, blank=True, choices=BL_CAIMAPS, unique=True)
    requested_bl_caimap = models.IntegerField(null=True, blank=True, choices=BL_CAIMAPS)
    
    # baseline drx fields
    current_drxbbpr0 = models.OneToOneField(DRX, related_name='current_drxbbpr0', null=True, blank=True)
    current_drxbbpr1 = models.OneToOneField(DRX, related_name='current_drxbbpr1', null=True, blank=True)
    current_drxbbpr2 = models.OneToOneField(DRX, related_name='current_drxbbpr2', null=True, blank=True)
    current_drxbbpr3 = models.OneToOneField(DRX, related_name='current_drxbbpr3', null=True, blank=True)

    requested_drxbbpr0 = models.ForeignKey(DRX, related_name='requested_drxbbpr0', null=True, blank=True)
    requested_drxbbpr1 = models.ForeignKey(DRX, related_name='requested_drxbbpr1', null=True, blank=True)
    requested_drxbbpr2 = models.ForeignKey(DRX, related_name='requested_drxbbpr2', null=True, blank=True)
    requested_drxbbpr3 = models.ForeignKey(DRX, related_name='requested_drxbbpr3', null=True, blank=True)

    # aca caimap fields
    current_aca_caimap = models.IntegerField(null=True, blank=True, choices=ACA_CAIMAPS, unique=True)
    requested_aca_caimap = models.IntegerField(null=True, blank=True, choices=ACA_CAIMAPS)

    # baseline dtsr fields
    current_dtsrbbpr0 = models.OneToOneField(DTSR, related_name='current_dtsrbbpr0', null=True, blank=True)
    current_dtsrbbpr1 = models.OneToOneField(DTSR, related_name='current_dtsrbbpr1', null=True, blank=True)
    current_dtsrbbpr2 = models.OneToOneField(DTSR, related_name='current_dtsrbbpr2', null=True, blank=True)
    current_dtsrbbpr3 = models.OneToOneField(DTSR, related_name='current_dtsrbbpr3', null=True, blank=True)

    requested_dtsrbbpr0 = models.ForeignKey(DTSR, related_name='requested_dtsrbbpr0', null=True, blank=True)
    requested_dtsrbbpr1 = models.ForeignKey(DTSR, related_name='requested_dtsrbbpr1', null=True, blank=True)
    requested_dtsrbbpr2 = models.ForeignKey(DTSR, related_name='requested_dtsrbbpr2', null=True, blank=True)
    requested_dtsrbbpr3 = models.ForeignKey(DTSR, related_name='requested_dtsrbbpr3', null=True, blank=True)

    def __unicode__(self):
        return '%s'%self.name

class PAD(models.Model):
    name = models.CharField(max_length=5)
    currentAntenna = models.OneToOneField(Antenna, related_name='current_pad_configuration', null=True, blank=True)
    requestedAntenna = models.ForeignKey(Antenna, related_name='requested_pad_configuration', null=True, blank=True)
    ste = models.ForeignKey(STE, null=True, blank=True)

    def __unicode__(self):
        return 'PAD %s'%self.name

class SAS_LLC(models.Model):
    name = models.CharField(max_length=100)
    currentAntenna = models.OneToOneField(Antenna, related_name='current_configuration_sas_llc', null=True, blank=True)
    requestedAntenna = models.ForeignKey(Antenna, related_name='requested_configuration_sas_llc', null=True, blank=True)
    ste = models.ForeignKey(STE, null=True, blank=True)

    def __unicode__(self):
        return 'SAS/LLC %s'%self.name
