from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('aRAT.apps.webServices',
    url(r'^ws/checkConsistency$', 'checkConsistency.views.check_consistency_service', name='ws_check_consistency'),
    url(r'^ws/blockUnblock$', 'blockUnblock.views.block_unblock_service', name='ws_block_unclock'),
    url(r'^ws/changesPage$', 'changesPage.views.changes_page_service', name='ws_changes_page'),
    url(r'^ws/applyChanges$', 'applyChanges.views.apply_changes_service', name='ws_apply_changes'),
)    
    
