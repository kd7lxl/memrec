from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^mission/mission/(?P<mission_id>\d+)/emd078', 'memrec.mission.admin_views.emd078'),
    (r'^', include(admin.site.urls)),
)
