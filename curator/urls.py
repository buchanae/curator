from django.conf.urls import patterns, include, url

from blueprints.api import api


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'curator.blueprints.views.test', name='home'),
    # url(r'^curator/', include('curator.foo.urls')),

    url(r'^api/', include(api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
