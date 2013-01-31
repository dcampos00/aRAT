from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('aRAT.apps.home.views',
    url(r'^$', 'home_view', name='home_view'),
    url(r'^padConfiguration$', 'pad_configuration_view', name='pad_configuration_view'),
    url(r'^steConfiguration$', 'ste_configuration_view', name='ste_configuration_view'),
    url(r'^corrConfiguration$', 'corr_configuration_view', name='corr_configuration_view'),
    url(r'^cloConfiguration$', 'clo_configuration_view', name='clo_configuration_view'),

    # Log In user
    url(r'^login$', 'login_user_view', name="login_user_view"),
    url(r'^logout$', 'logout_user_view', name="logout_user_view")
)
