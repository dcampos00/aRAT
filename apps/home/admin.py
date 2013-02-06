from django.contrib import admin
from aRAT.apps.home.models import Antenna, PAD, Correlator, CentralLO

admin.site.register(Antenna)
admin.site.register(PAD)
admin.site.register(Correlator)
admin.site.register(CentralLO)
