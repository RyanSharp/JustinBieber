from django.conf.urls import *

urlpatterns = patterns('',
	(r'^checkUrl/([A-Za-z0-9_\.-]+)$', 'youtube.views.checkForYouTube'),
	(r'^youtubeStats/([A-Za-z0-9_\.-]+)$', 'youtube.views.getYouTubeStats'),
	(r'^oauth2callback', 'youtube.views.oauthCallBack'),
	(r'^getAccess/([A-Za-z0-9_\.-]+)$', 'youtube.views.getAccess'),
)