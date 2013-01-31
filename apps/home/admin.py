from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, STE, SAS_LLC, DTSR, DRX

admin.site.register(Antenna)
admin.site.register(PAD)
admin.site.register(STE)
admin.site.register(DRX)
admin.site.register(SAS_LLC)
admin.site.register(DTSR)
