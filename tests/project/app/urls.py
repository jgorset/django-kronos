from django.conf.urls.defaults import *

from views import home

urlpatterns = patterns('',
    url(r'^$', home, name='home'),

    url('fandjango/', include('fandjango.urls'))
)
