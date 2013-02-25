from django.db import models

COMMON_SETTINGS = (
    (u'BLOCK', u'Block'),
    )


class Configuration(models.Model):
    """
    Model that allows to define the settings of the application.
    For now this model is useful to stores the status (block/unblock)
    of the system
    """

    # name of the setting that will be stored
    setting = models.CharField(max_length=5,
                               choices=COMMON_SETTINGS,
                               unique=True)
    # boolean value of the setting that will be stored
    value = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.setting
