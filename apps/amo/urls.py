import csp.views
from waffle.views import wafflejs

from django.conf.urls.defaults import patterns, url, include
from django.views.decorators.cache import never_cache

from django_statsd.urls import urlpatterns as statsd_patterns

from . import views

services_patterns = patterns('',
    url('^monitor(.json)?$', never_cache(views.monitor),
        name='amo.monitor'),
    url('^loaded$', never_cache(views.loaded), name='amo.loaded'),
    url('^csp/policy$', csp.views.policy, name='amo.csp.policy'),
    url('^csp/report$', views.cspreport, name='amo.csp.report'),
    url('^builder-pingback', views.builder_pingback,
        name='amo.builder-pingback'),
    url('^graphite/(addons|dev|stage|apps-preview|apps-preview-dev)$',
        views.graphite, name='amo.graphite'),
    url('^timing/', include(statsd_patterns)),
)

urlpatterns = patterns('',
    url('^robots.txt$', views.robots, name='robots.txt'),
    url(r'^wafflejs$', wafflejs, name='wafflejs'),
    ('^services/', include(services_patterns)),

    url('^opensearch.xml$', 'api.views.render_xml',
                            {'template': 'amo/opensearch.xml'},
                            name='amo.opensearch'),

)
