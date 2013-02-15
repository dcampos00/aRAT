from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

#Dajaxice
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from aRAT.apps.home.admin import custom_admin_site

urlpatterns = patterns('',
    # Web Services URLs
    url(r'^', include('aRAT.apps.webServices.urls')),
    url(r'^', include('aRAT.apps.home.urls')),

    # Admin
    url(r'^admin/', include(custom_admin_site.urls)),

    # Dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
