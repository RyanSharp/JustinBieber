from django.conf.urls import *

urlpatterns = patterns('',
	(r'^connect$', 'facebook.views.facebookConnect'),
	(r'^scrape$', 'facebook.views.queryAPI'),
)