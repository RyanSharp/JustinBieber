from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'urlcheck.views.home', name='home'),
    # url(r'^urlcheck/', include('urlcheck.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', include('fbsharing.urls')),
    url(r'^yt/', include('youtube.urls')),
    url(r'^facebook/', include('facebook.urls')),
)
