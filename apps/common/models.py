from django.db import models

COMMON_SETTINGS = (
    (u'BLOCK', u'Block'),
    )

# Create your models here.
class Configuration(models.Model):
    """
    Model that define the settings of the application, e.g: status of the system
    block and unblock
    """

    setting = models.CharField(max_length=5, choices=COMMON_SETTINGS, unique=True)
    value = models.BooleanField(default=False)

    def __unicode__(self):
        return self.setting
