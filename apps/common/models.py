from django.db import models

# Create your models here.
class settings(models.Model):
    """
    Model that define the settings of the application, e.g: status of the system
    block and unblock
    """    
    
    COMMON_SETTINGS = (
        ('BLOCK', 'Block'),
        )

    setting = models.CharField(max_length=5, choices=COMMON_SETTINGS, unique=True)
    value = models.BooleanField(default=False)

    def __unicode__(self):
        return self
