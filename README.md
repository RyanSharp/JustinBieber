JustinBieber
============

THE MODELS:

The goal of this Engagement Tool is to be able to track engagement statistics for ANY url (not just YouTube).  YouTube statistics will not be available for non-YouTube
	urls, obviously, but all other API's will give responses regardless of the link's origins.

This version of the Engagement tool can provide non-YouTube data for any link provided by the user.  To recieve YouTube data, youtube links MUST be of some variation of
	www.youtube.com, so urls like yout.ube currently do not work.

We currently have 3 models that exist in the fbsharing app:
	Campaign, fbDataRequest, DailyRun

Only the fbDataRequest is currently truly being used.  When a user inputs a url on the input page, ("http://" + request.META["HTTP_HOST"] + "/fb/inputUrl"),
	a new fbDataRequest object is created and all the information for that link is pulled from the various API's.

This tool currently accesses the following API's:
	1. YouTube
	2. Facebook
	3. Twitter
	4. Google Plus
	5. Pinterest
	6. LinkedIn
	7. Stumble Upon

Since we only use the fbDataRequest model, this system can do no more than just track the current engagement statistics for a url.  In order to track one url over
	several days, we will have to use the Campaign model.  My intention is to use the Campaign model as a cummulative total for engagement statistics and the
	Campaign model is accompanied by a fbDataRequest model for each day the campaign is being run (ex. if the Campaign runs for 7 days, that Campaign should have 
	7 fbDataRequest models that accompany it).  Each fbDataRequest model will act as a daily change in stats, in other words the engagement statistics in the 
	fbDataRequest model should equal the current statistics minus the Campaign's running total.  This way, we can use the Campaign model to display the current 
	engagement statistics and use the fbDataRequest models to show the daily change.

Ultimately, this tool will also need to be able to pull engagement statistics for entire YouTube playlists & channels.  Currently, functions capable of pulling all
	video ID's from a channel or playlist have been implemented, but there are no functions that tie this functionality to the actual engagement tool.