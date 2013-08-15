# Create your views here.
import hashlib
import urllib
import urllib2
import urlparse
import twitter
import base64
import httplib
import json
import requests
import httplib

import oauth2 as oauth

import ast

from apiclient.discovery import build

from optparse import OptionParser
from fbsharing.models import fbDataRequest, Campaign
from fbsharing.forms import dataForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from pprint import pprint

'''
YOUTUBE_SCOPE       = "https://www.googleapis.com/auth/yt-analytics.readonly"
API_SERVICE_NAME    = "youtubeAnalytics"
API_VERSION         = "v1"
'''

YOUTUBE_SCOPE       = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME    = "youtube"
API_VERSION         = "v3"

CLIENT_ID           = "466813789589.apps.googleusercontent.com"
API_KEY             = "AIzaSyAIy-ICPQKvFm6WMMaL9dj8KdhvpWWRecs"
CLIENT_SECRET       = "YdwplMncxj94h3TkqLe3R7Yo"

STATISTICS_URL      = "https://www.googleapis.com/youtube/v3/videos"

ACCESS_TOKEN_URL    = "https://accounts.google.com/o/oauth2/token"
REQUEST_ACCESS_URL  = "https://accounts.google.com/o/oauth2/auth?scope="
REDIRECT_URI        = "http://localhost:8080/yt/oauth2callback"



def convertString(myString):
    outString = ""
    for char in myString:
        if char == "/":
            outString += "%" + "2F"
        elif char == ":":
            outString += "%" + "3A"
        else:
            outString += char
    return outString


def checkForYouTube(data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        site = "http://www.youtube.com"
        path = ""
        if data.url[:22] == "http://www.youtube.com":
            path = data.url[22:]
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
        data.url = "http://www.youtube.com" + path
        data.save()
        return response.status == 200
    except Exception, e:
        print e
    return False


def getVideoID(videoURL):
    return videoURL[31:]


def getAccess(request, data_id):
    if checkForYouTube(data_id):
        request_url = REQUEST_ACCESS_URL + convertString(YOUTUBE_SCOPE) + "&state=" + data_id + "&redirect_uri=" + REDIRECT_URI + "&response_type=code&client_id=" + CLIENT_ID + "&approval_prompt=auto&access_type=offline"
        return HttpResponseRedirect(request_url)
    return redirect('fbsharing.views.displayStats', data_id)


def oauthCallBack(request):
    code = request.GET['code']
    state = request.GET['state']
    request_url = ACCESS_TOKEN_URL + "code=" + code + "&client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&redirect_uri=" + REDIRECT_URI + "&grant_type=authorization_code"
    try:
        values = dict(code=code,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,grant_type='authorization_code')
        data = urllib.urlencode(values)
        req = urllib2.Request(ACCESS_TOKEN_URL,data)
        resp = urllib2.urlopen(req)
        content = resp.read()
        new_dic = ast.literal_eval(content)
        access_token = new_dic["access_token"]
        myData = fbDataRequest.objects.get(pk=int(state))
        vid_id = getVideoID(myData.url)
    except Exception, e:
        print e
    return redirect('fbsharing.views.displayStats', state)


def getYouTubeStats(request, data_id):
    if checkForYouTube(data_id):
        try:
            myData = fbDataRequest.objects.get(pk=data_id)
            vid_id = getVideoID(myData.url)
            my_url = STATISTICS_URL + "?id=" + vid_id + "&part=statistics&field=monetizationDetails" + "%" + "2Cstatistics&key=" + API_KEY
            r = urllib2.urlopen(my_url)
            response = ast.literal_eval(r.read())
            myData.yt_comment_count = response['items'][0]['statistics']['commentCount']
            myData.yt_view_count = response['items'][0]['statistics']['viewCount']
            myData.yt_fav_count = response['items'][0]['statistics']['favoriteCount']
            myData.yt_dislike_count = response['items'][0]['statistics']['dislikeCount']
            myData.yt_like_count = response['items'][0]['statistics']['likeCount']
            myData.save()
        except Exception, e:
            print e
    return redirect('fbsharing.views.displayStats', data_id)


def getChannelVideos(request, channel_id):
    # Some code goes here
    url = "https://www.googleapis.com/youtube/v3/playlists?"


def getPlaylistVideos(request, playlist_id):
    try:
        url = "https://gdata.youtube.com/feeds/api/playlists/" + playlist_id + "?v=2"
    except Exception, e:
        raise e
    # Some code goes here