from django.conf.urls import *

urlpatterns = patterns('',
	#(r'^getStats/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getStats'),
	(r'^inputUrl$', 'fbsharing.views.getFacebookStats'),
	#(r'^getTweets/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getTwitterStats'),
	(r'^display/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.displayStats'),
	#(r'^stumbleUpon/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getStumbledUponStats'),
	#(r'^pinterest/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getPinterestStats'),
	#(r'^recentTweets/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getRecentTweets'),
	#(r'^newCampaign$', 'fbsharing.views.addCampaign'),
	#(r'^startCampaign/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.initializeCampaign'),
	#(r'^socialShares/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.socialShares'),
	#(r'^youtube/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.youtube'),
	#(r'^campaign/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.viewCampaign'),
	(r'^betterStats/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getBetterFacebookStats'),
	#(r'^oneTimeYouTube/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.oneTimeYouTubeStats'),
	#(r'^linkedin/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getLinkedInShares'),
	#(r'^gplus/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.getGPlusOnes'),
	(r'^dataPull/([A-Za-z0-9_\.-]+)$', 'fbsharing.views.pullAllStats'),
	(r'^playlist$', 'fbsharing.views.getYouTubePlaylist'),
	(r'^channel$', 'fbsharing.views.getChannelVideos'),
)