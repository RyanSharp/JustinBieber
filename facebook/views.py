# Create your views here.
import hashlib
import urllib
import urllib2
import urlparse
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
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from pprint import pprint
from datetime import date

# Facebook API info & urls
APP_ID                  = "441109929301348"
APP_SECRET              = "8c218d00b2384a38c7938e4b74156da1"

ACCESS_TOKEN_URL        = "https://graph.facebook.com/oauth/access_token?"
REQUEST_TOKEN_URL       = "https://www.facebook.com/dialog/oauth?"
GRAPH_SEARCH_URL        = "https://graph.facebook.com/search?"
GRAPH_API_URL           = "https://graph.facebook.com/"


permissions = ["user_checkins", "user_events", "user_groups", "user_hometown", "user_interests",
               "user_likes", "user_location", "user_photos", "user_status"]

ignore_list = ["approved_friend", "app_created_story"]

ignore_words = ["likes", "activated", "updated", '"liked"']

hit_list = "posted a link"


def facebookConnect(request):
    callback_url = "http://%s/facebook/scrape" % request.META['HTTP_HOST']
    return HttpResponseRedirect( "%sclient_id=%s&client_secret=%s&scope=publish_stream&redirect_uri=%s" % (REQUEST_TOKEN_URL, APP_ID, APP_SECRET, callback_url))


def queryAPI(request):
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = "http://%s/facebook/scrape" % request.META['HTTP_HOST']
    request_url =  "%sclient_id=%s&client_secret=%s&scope=publish_stream&redirect_uri=%s&code=%s" % (ACCESS_TOKEN_URL, APP_ID, APP_SECRET, redirect_uri, code)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    query_url = "%sq=%s&type=%s&access_token=%s" % (GRAPH_SEARCH_URL, "mobile", "post", access_token)
    content = urllib.urlopen(query_url)
    data = json.load(content)
    for item in data["data"]:
        if "comments" in item:
            for comment in item["comments"]["data"]:
                new_query_url = GRAPH_API_URL + "%s/posts?access_token=%s" % (str(comment["from"]["id"]), access_token)
                new_content = urllib.urlopen(new_query_url)
                new_data = json.load(new_content)
                for stuff in new_data["data"]:
                    if "category" in stuff["from"]:
                        continue
                    elif "status_type" in stuff:
                        if stuff["status_type"] in ignore_list:
                            continue
                        print stuff
                        print ""
                    elif "story" in stuff:
                        useful = True
                        if hit_list in stuff["story"]:
                            hit_query = GRAPH_API_URL + "%s?access_token=%s" % (stuff["id"], access_token)
                            hit_content = urllib.urlopen(hit_query)
                            print "USER POSTED"
                            print json.load(hit_content)
                            print ""
                            continue
                        for word in ignore_words:
                            if word in stuff["story"]:
                                useful = False
                                break
                        if useful:
                            print "USER ACTION"
                            print stuff
                            print ""
                    elif "link" in stuff:
                        print stuff
                    else:
                        print "OTHER"
                        print stuff
                        print ""
    return HttpResponse(json.dumps(data))
