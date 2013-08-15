# Create your views here.
import hashlib
import urllib
import urllib2
import urlparse
import twitter
import base64
import httplib
import json
import tweepy
import time

from urllib2 import urlopen

import oauth2 as oauth

import ast

from xml.etree.ElementTree import fromstring

from httplib2 import Http

from fbsharing.models import fbDataRequest, Campaign, DailyRun
from fbsharing.forms import dataForm, CampaignForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from pprint import pprint
from datetime import date


# Facebook API info & urls
APP_ID                  = "441109929301348"
APP_SECRET              = "8c218d00b2384a38c7938e4b74156da1"

ACCESS_TOKEN_URL        = "https://graph.facebook.com/oauth/access_token"
REQUEST_TOKEN_URL       = "https://www.facebook.com/dialog/oauth"
CHECK_AUTH              = "https://graph.facebook.com/me"
GRAPH_URL               = "https://graph.facebook.com/"
VIEW_POSTS_URL          = "https://graph.facebook.com/search?access_token="
FB_GET_URL              = "https://graph.facebook.com/?id="
ANOTHER_FB_URL          = "https://api.facebook.com/method/fql.query?query="
ALT_QUERY_URL           = "https://api-read.facebook.com/restserver.php?method=fql.query&query="


# Twitter API info & urls
TWITTER_CONSUMER_KEY    = '8nY1q44v3YWGgqfP2eCjFg'
TWITTER_CONSUMER_SECRET = 's2MFyXSLbHTmGbz9qBGNFubaeTRivsLJpHsnESnlfE'
TWITTER_ACCESS_KEY      = '1535252624-YWB7X7lbBwdmzKmWA5Aiep7wis3ARc0EA8hDqIj'
TWITTER_ACCESS_SECRET   = 'MBrOvB34fuQtQ8vzyfMcA48ZbEhg3zpqgMvAuTSDDk'

TWITTER_SEARCH_URL      = "http://cdn.api.twitter.com/1/urls/count.json?url="
TWITTER_ACCESS_TOKEN_URL= "https://api.twitter.com/oauth/access_token"
TWEET_SEARCH_URL        = "https://api.twitter.com/1.1/search/tweets.json?q="

# Google API urls
API_KEY                 = "AIzaSyAIy-ICPQKvFm6WMMaL9dj8KdhvpWWRecs"
STATISTICS_URL          = "https://www.googleapis.com/youtube/v3/videos"
GOOG_PLUS_STATS         = "https://clients6.google.com/rpc?key=" + API_KEY
CLIENT_ID               = "466813789589.apps.googleusercontent.com"
CLIENT_SECRET           = "YdwplMncxj94h3TkqLe3R7Yo"
REDIRECT_URI            = "http://localhost:8080/fb/gredirect"
GOOG_SCOPE              = "https://www.googleapis.com/auth/plus.login"
GOOG_ACT_SEARCH         = "https://www.googleapis.com/plus/v1/activities"


# Verify that the link provided by user does not return an error (error code 400 or greater)
def linkValid(urlString):
    code = urlopen(urlString).code
    if (int(code)/100 >= 4):
        return False
    return True

# Convert url to form readable by some api's (other APIs can take in a regular url)
def convertString(myString):
    outString = ""
    for char in myString:
        if char == "/":
            outString += "%" + "2F"
        elif char == ":":
            outString += "%" + "3A"
        elif char == "?":
            outString += "%" + "3F"
        elif char == "=":
            outString += "%" + "3D"
        else:
            outString += char
    return outString

# Determines whether or not the link provided is a youtube link
def checkForYouTube(data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        site = "http://www.youtube.com"
        path = ""
        # Checking all possibilities for youtube links.  Still need to add the yout.ube links
        if data.url[:22] == "http://www.youtube.com":
            path = data.url[22:]
        elif data.url[:23] == "https://www.youtube.com":
            path = data.url[23:]
        elif data.url[:15] == "www.youtube.com":
            path = data.url[15:]
        elif data.url[:11] == "youtube.com":
            path = data.url[11:]
        else:
            return False
        conn = httplib.HTTPConnection("www.youtube.com")
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
        # Use urlparse to separate site and path segments of the url
        o = urlparse.urlparse(data.url)
        found = False
        tag = False
        video_query = "v="
        for char in o.query:
            if char == "v" and not found:
                found = True
                tag = True
            elif char == "=" and tag:
                tag = False
            elif found and char == "&":
                found = False
            elif found and not tag and char != "&":
                video_query += char
        data.url = "http://www.youtube.com/watch?" + video_query
        data.save()
        return response.status == 200
    except Exception as e:
        print e
    return False

# Reformats a YouTube url to the standard (http://www.youtube.com/watch?v=VID_ID)
def convertYouTubeURL(url):
    o = urlparse.urlparse(url)
    found = False
    tag = False
    video_query = "v="
    for char in o.query:
        if char == "v" and not found:
            found = True
            tag = True
        elif char == "=" and tag:
            tag = False
        elif found and char == "&":
            found = False
        elif found and not tag and char != "&":
            video_query += char
    return "http://www.youtube.com/watch?" + video_query


# If the url does not begin with http or https, this function adds it in
def makeHttp(data_id):
    new_url = "http://"
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        if data.url[:4] != "http":
            new_url += data.url
            data.url = new_url
            data.save()
    except Exception as e:
        return "Error"
    return data.url

# Returns the section of the YouTube URl that contains the video ID
def getVideoID(videoURL):
    return videoURL[31:]

# If request is a POST, this function makes initial call to the Facebook API to receive a code to exchange for an Access Token
def getFacebookStats(request):
    facebook = fbDataRequest()
    if request.method == 'POST':
        if linkValid(request.POST['url']):
            form = dataForm(request.POST, instance=facebook)
            if form.is_valid():
                try:
                    facebook = form.save()
                    # return redirect('fbsharing.views.getRecentTweets', facebook.id)
                    callback_url = 'http://' + request.META['HTTP_HOST'] + '/fb/betterStats/' + str(facebook.id)
                    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))
                except Exception as e:
                    print "Data Request object failed to save"
    form = dataForm(instance=facebook)
    return render_to_response('fbsharing/fb_url_form.html', {'form': form} , context_instance=RequestContext(request))

# This function is called after all data has been gathered, displays all info on a page
def displayStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception as e:
        print e
    facebook = fbDataRequest()
    form = dataForm(instance=facebook)
    return render_to_response('fbsharing/url_form.html', {'form': form, 'data': data}, context_instance=RequestContext(request))

# Callback function for Facebook API.  Exchanges a code for FB Access Token and then makes a call to the FQL API for share counts (FQL = Facebook Query Language)
def getBetterFacebookStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        if checkForYouTube(data_id):
            data.url = convertYouTubeURL(data.url)
            data.save()
    except Exception as e:
        print e
    # Parsing code from API response to our initial request for access
    code = request.GET.get('code')
    # Setting up OAuth client to connect to the FQL API
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = "https://" + request.META['HTTP_HOST'] + '/fb/getBetterFacebookStats/' + data_id
    # Prepare Access Token request URL (Must supply same redirect URI as initial request for access)
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    # Parse Access Token from the API's response to access token request
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        # Preparing components of FQL API requeset url
        request_params = "S" + "ELECT+click_count,comment_count,like_count,share_count,total_count"
        request_api = "+FROM+link_stat+WHERE+url="
        request_target = '"' + data.url + '"'
        request_url2 = ALT_QUERY_URL + request_params + request_api + request_target + "&access_token=" + access_token
        resp, cont = client.request(request_url2, 'GET')
        root = fromstring(cont)
        # Iterate through XML response looking for the share, like, and comment fields
        for child in root:
            for unit in child:
                if unit.tag == "{http://api.facebook.com/1.0/}comment_count":
                    data.facebook_comments = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}like_count":
                    data.facebook_likes = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}share_count":
                    data.facebook_shares = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}total_count":
                    data.facebook_total = int(unit.text)
                #elif unit.tag == "{http://api.facebook.com/1.0/}click_count":
                #    print unit.text
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.pullAllStats', data_id)

# Connects to all non-Facebook APIs (Twitter, Pinterest, LinkedIn, Stumble Upon, Google+, YouTube)
def pullAllStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception as e:
        return render_to_response('fbsharing/error_page.html', {'text': 'Queried Data Object Could Not Be Found'}, context_instance=RequestContext(request))
    try:
        # Setup OAuth client to connect to Twitter REST API
        consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer)
        request_url = TWITTER_SEARCH_URL + data.url
        resp, cont = client.request(request_url, 'GET')
        # Check if response is successful
        if resp['status'] == '200':
            new_dic = ast.literal_eval(cont)
            # Parse Tweet count from API response
            data.tweets = int(new_dic['count'])
            data.save()
        else:
            print "Twitter API call failed"
    except Exception as e:
        print "Twitter Failure"
        print e
    try:
        content = urllib.urlopen("http://www.stumbleupon.com/services/1.01/badge.getinfo?url=" + data.url)
        cont_data = json.load(content)
        # Check is required since API response is differs based on whether or not the link exists in their database
        if cont_data['result']['in_index'] == False:
            data.stumble = 0
            data.save()
        else:
            data.stumble = int(cont_data['result']['views'])
            data.save()
    except Exception as e:
        print "Stumble Upon Failure"
        print e
    try:
        # Receive response from Pinterest API call
        content = urllib.urlopen("http://api.pinterest.com/v1/urls/count.json?callback=&url=" + data.url).read()
        new_dic = ast.literal_eval(content)
        data.pins = int(new_dic['count'])
        data.save()
    except Exception as e:
        print "Pinterest Failure"
        print e
    try:
        # Request to linked in API
        content = urllib.urlopen("http://www.linkedin.com/countserv/count/share?url=" + data.url + "&format=json").read()
        new_dic = ast.literal_eval(content)
        data.linkedin = int(new_dic['count'])
        data.save()
    except Exception as e:
        print "LinkedIn Failure"
        print e
    try:
        # Open html page for Google+ Plus One Button for a specific URL
        request_url = "https://plusone.google.com/u/0/_/+1/fastbutton?url=" + convertString(data.url)
        content = urllib.urlopen(request_url).read()
        point = 1400
        searching = True
        while(point < 1800 and searching):
            # Search for specific key in the G+ Button HTML page
            if content[point:point+19] == "window.__SSR = {c: ":
                count = 0
                # Once count has been found on page, parse actual data from html
                while(searching):
                    if content[point+19+count:point+20+count] == ' ':
                        data.g_plus_one = int(content[point+19:point+17+count])
                        data.save()
                        searching = False
                    else:
                        count += 1
            point += 1
    except Exception, e:
        print "Google+ Failure"
        print e
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        # API request to youtube will only be made if the link has been verified as a YouTube URL
        if checkForYouTube(data_id):
            my_url = STATISTICS_URL + "?id=" + getVideoID(data.url) + "&part=statistics&field=monetizationDetails" + "%" + "2Cstatistics&key=" + API_KEY
            r = urllib2.urlopen(my_url)
            response = ast.literal_eval(r.read())
            data.yt_comment_count = int(response['items'][0]['statistics']['commentCount'])
            data.yt_view_count = int(response['items'][0]['statistics']['viewCount'])
            data.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount'])
            data.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount'])
            data.yt_like_count = int(response['items'][0]['statistics']['likeCount'])
            data.save()
    except Exception as e:
        print "YouTube Failure"
        print e
    try:
        data.save()
    except Exception as e:
        return render_to_response('fbsharing/error_page.html', {'text': 'Data Request Object Failed to save properly.  Info for this session was not recorded'}, context_instance=RequestContext(request))
    return redirect('fbsharing.views.displayStats', data_id)

# Returns list of video IDs contained in a youtube playlist (requires playlist ID in the request)
def getYouTubePlaylist(request):
    if request.method == 'POST':
        url = "https://gdata.youtube.com/feeds/api/playlists/" + request.POST['playlist_id'] + "?v=2"
        try:
            r = urllib2.urlopen(url)
            root = fromstring(r.read())
            for child in root:
                for unit in child:
                    if unit.tag == '{http://www.w3.org/2005/Atom}id':
                        item_id = returnPlaylistItemID(unit.text, request.POST['playlist_id'])
                        if not item_id == '':
                            video_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&id=" + item_id + "&key=" + API_KEY
                            response = urllib2.urlopen(video_url)
                            my_dic = ast.literal_eval(response.read())
                            print my_dic['items'][0]['snippet']['resourceId']['videoId']
        except Exception, e:
            print e
        return redirect('fbsharing.views.getYouTubePlaylist')
    return render_to_response('fbsharing/input_playlist.html', {}, context_instance=RequestContext(request))

# Parse Video ID's from the json response for Playlist content
def returnPlaylistItemID(video_tag, playlist_id):
    count = 0
    while(True):
        if video_tag[count:count+len(playlist_id)] == playlist_id:
            return video_tag[count+len(playlist_id)+1:]
        elif count >= len(video_tag):
            return ""
        else:
            count+=1
    return ""

# Returns list of all video IDs from a YouTube channel (requires Channel ID)
def getChannelVideos(request):
    if request.method == 'POST':
        url = "https://gdata.youtube.com/feeds/api/users/" + request.POST['channel_id'] + "/uploads"
        try:
            r = urllib2.urlopen(url)
            root = fromstring(r.read())
            for child in root:
                for unit in child:
                    if unit.tag == "{http://www.w3.org/2005/Atom}id":
                        video_id = ripVidIDFromChannelFeed(unit.text)
                        print video_id
            return redirect('fbsharing.views.getChannelVideos')
        except Exception, e:
            print e
    return render_to_response('fbsharing/input_channel.html', {}, context_instance=RequestContext(request))

# Parse Video ID's from the json response for Channel content
def ripVidIDFromChannelFeed(feed_url):
    o = urlparse.urlparse(feed_url)
    return o.path[18:]
