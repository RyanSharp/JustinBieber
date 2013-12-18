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


def linkValid(urlString):
    code = urlopen(urlString).code
    if (int(code)/100 >= 4):
        return False
    return True


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


def checkForYouTube(data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        site = "http://www.youtube.com"
        path = ""
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


def getVideoID(videoURL):
    return videoURL[31:]


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


def updateCampaigns(request):
    try:
        campaigns = Campaign.objects.filter(current=True)
        today = date.today()
        daily = DailyRun(more=False)
        for campaign in campaigns:
            if today > campaign.end_date:
                campaign.current = False
                campaign.save()
            elif daily.more == False:
                daily.more=True
                daily.pending = campaign.id + ""
            else:
                daily.pending += "," + campaign.id
        daily.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.dailyIterate', daily.id)


def dailyIterate(request, daily_id):
    try:
        daily = DailyRun.objects.get(pk=daily_id)
        count = 0
        if daily.more:
            for char in daily.pending:
                if char == ",":
                    if daily.completed is None:
                        daily.completed = daily.pending[:count-1]
                    else:
                        daily.completed = "," + daily.pending[:count-1]
                    toRun = int(daily.pending[:count-1])
                    daily.current = Campaign.objects.get(pk=toRun)
                    daily.pending = daily.pending[count:]
                    daily.save()
                    return redirect('fbsharing.views.getDailyStats', daily.id)
            daily.more = False
            daily.current = Campaign.objects.get(pk=int(daily.pending))
            if daily.completed is None:
                daily.completed = daily.pending
            else:
                daily.completed = "," + daily.pending
            daily.pending = ""
            daily.save()
            return redirect('fbsharing.views.getDailyStats', daily.id)
    except Exception as e:
        print e


def getDailyStats(daily_id):
    try:
        daily = DailyRun.objects.get(pk=daily_id)
        campaign = daily.current
        data = fbDataRequest(campaign=campaign, url=campaign.url)
    except Exception as e:
        print e
    try:
        consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer)
        request_url = TWITTER_SEARCH_URL + data.url
        resp, cont = client.request(request_url, 'GET')
        if resp['status'] == '200':
            new_dic = ast.literal_eval(cont)
            data.tweets = int(new_dic['count']) - campaign.tweets
            campaign.tweets = int(new_dic['count'])
        else:
            print "Twitter API call failed"
    except Exception as e:
        print e
    try:
        content = urllib.urlopen("http://www.stumbleupon.com/services/1.01/badge.getinfo?url=" + data.url)
        cont_data = json.load(content)
        if cont_data['result']['in_index'] == False:
            data.stumble = 0
        else:
            data.stumble = int(cont_data['result']['views']) - campaign.stumble
            campaign.stumble = int(cont_data['result']['views'])
    except Exception as e:
        print e
    try:
        content = urllib.urlopen("http://api.pinterest.com/v1/urls/count.json?callback=&url=" + data.url).read()
        new_dic = ast.literal_eval(content)
        data.pins = int(new_dic['count']) - campaign.pins
        campaign.pins = int(new_dic['count'])
    except Exception as e:
        print e
    try:
        content = urllib.urlopen("http://www.linkedin.com/countserv/count/share?url=" + data.url + "&format=json").read()
        new_dic = ast.literal_eval(content)
        data.linkedin = int(new_dic['count']) - campaign.linkedin
        campaign.linkedin = int(new_dic['count'])
    except Exception as e:
        print e
    try:
        request_url = GOOG_ACT_SEARCH + "?query=" + convertString(data.url) + "&key=" + API_KEY
        content = urllib.urlopen(request_url).read()
        new_dic = ast.literal_eval(content)
        for item in new_dic['items']:
            if makeHttp(data_id) == item['object']['attachments'][0]['url']:
                activity_id = item['id']
                request_url2 = GOOG_ACT_SEARCH + "/" + activity_id + "?key=" + API_KEY
                content2 = urllib.urlopen(request_url2).read()
                dic = ast.literal_eval(content2)
                data.g_reshares = int(dic['object']['resharers']['totalItems']) - campaign.g_reshares
                data.g_plus_one = int(dic['object']['plusoners']['totalItems']) - campaign.g_plus_one
                data.g_replies = int(dic['object']['replies']['totalItems']) - campaign.g_replies
                campaign.g_reshares = int(dic['object']['resharers']['totalItems'])
                campaign.g_plus_one = int(dic['object']['plusoners']['totalItems'])
                campaign.g_replies = int(dic['object']['replies']['totalItems'])
    except Exception as e:
        print e
    try:
        my_url = STATISTICS_URL + "?id=" + getVideoID(data.url) + "&part=statistics&field=monetizationDetails" + "%" + "2Cstatistics&key=" + API_KEY
        r = urllib2.urlopen(my_url)
        response = ast.literal_eval(r.read())
        data.yt_comment_count = int(response['items'][0]['statistics']['commentCount']) - campaign.yt_comment_count
        data.yt_view_count = int(response['items'][0]['statistics']['viewCount']) - campaign.yt_view_count
        data.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount']) - campaign.yt_fav_count
        data.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount']) - campaign.yt_dislike_count
        data.yt_like_count = int(response['items'][0]['statistics']['likeCount']) - campaign.yt_like_count
        campaign.yt_comment_count = int(response['items'][0]['statistics']['commentCount'])
        campaign.yt_view_count = int(response['items'][0]['statistics']['viewCount'])
        campaign.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount'])
        campaign.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount'])
        campaign.yt_like_count = int(response['items'][0]['statistics']['likeCount'])
    except Exception as e:
        print e
    try:
        data.save()
        campaign.save()
    except Exception as e:
        print e
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/fb/dailyFBStats/' + str(daily.id) + "/" + str(data.id)
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))


def dailyFBStats(request, daily_id, data_id):
    try:
        daily = DailyRun.objects.get(pk=daily_id)
        campaign = daily.campaign
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception as e:
        print e
    request_params = "S" + "ELECT+click_count,comment_count,like_count,share_count,total_count"
    request_api = "+FROM+link_stat+WHERE+url="
    request_target = '"' + data.url + '"'
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = "https://" + request.META['HTTP_HOST'] + '/fb/getBetterFacebookStats/' + data_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        request_url2 = ALT_QUERY_URL + request_params + request_api + request_target + "&access_token=" + access_token
        resp, cont = client.request(request_url2, 'GET')
        root = fromstring(cont)
        for child in root:
            for unit in child:
                if unit.tag == "{http://api.facebook.com/1.0/}click_count":
                    print unit.text
                elif unit.tag == "{http://api.facebook.com/1.0/}comment_count":
                    data.facebook_comments = int(unit.text) - campaign.facebook_comments
                    campaign.facebook_comments = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}like_count":
                    data.facebook_likes = int(unit.text) - campaign.facebook_likes
                    campaign.facebook_likes = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}share_count":
                    data.facebook_shares = int(unit.text) - campaign.facebook_shares
                    campaign.facebook_shares = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}total_count":
                    data.facebook_total = int(unit.text) - campaign.facebook_total
                    campaign.facebook_total = int(unit.text)
        data.save()
        campaign.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.dailyIterate', daily.id)


def displayStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception as e:
        print e
    facebook = fbDataRequest()
    form = dataForm(instance=facebook)
    return render_to_response('fbsharing/url_form.html', {'form': form, 'data': data}, context_instance=RequestContext(request))


def getStats(request, data_id):
    try:
        facebook = fbDataRequest.objects.get(pk=data_id)    
    except Exception as e:
        print e
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/fb/betterStats/' + data_id 
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        request_url = (FB_GET_URL + facebook.url)
        resp, cont = client.request(request_url, 'GET')     # Request share data for our url (or keyword)
        if resp['status'] == '200':
            new_dic = ast.literal_eval(cont)                # If request is received correctly, save fb share data into model
            facebook.fb_shares = int(new_dic['shares'])
            facebook.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.getRecentTweets', data_id)


def getBetterFacebookStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        if checkForYouTube(data_id):
            data.url = convertYouTubeURL(data.url)
            data.save()
    except Exception as e:
        print e
    request_params = "S" + "ELECT+click_count,comment_count,like_count,share_count,total_count"
    request_api = "+FROM+link_stat+WHERE+url="
    request_target = '"' + data.url + '"'
    code = request.GET.get('code')
    consumer = oauth.Consumer(key=APP_ID, secret=APP_SECRET)
    client = oauth.Client(consumer)
    redirect_uri = "https://" + request.META['HTTP_HOST'] + '/fb/getBetterFacebookStats/' + data_id
    request_url = ACCESS_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (APP_ID, APP_SECRET)
    resp, cont = client.request(request_url, 'GET')
    access_token = dict(urlparse.parse_qsl(cont))['access_token']
    try:
        # request_url2 = ANOTHER_FB_URL + request_params + request_api + request_target + "&access_token=" + access_token
        request_url2 = ALT_QUERY_URL + request_params + request_api + request_target + "&access_token=" + access_token
        resp, cont = client.request(request_url2, 'GET')
        root = fromstring(cont)
        for child in root:
            for unit in child:
                if unit.tag == "{http://api.facebook.com/1.0/}click_count":
                    print unit.text
                elif unit.tag == "{http://api.facebook.com/1.0/}comment_count":
                    data.facebook_comments = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}like_count":
                    data.facebook_likes = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}share_count":
                    data.facebook_shares = int(unit.text)
                elif unit.tag == "{http://api.facebook.com/1.0/}total_count":
                    data.facebook_total = int(unit.text)
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.pullAllStats', data_id)


def pullAllStats(request, data_id):
    print "where does it stop?"
    try:
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception as e:
        return render_to_response('fbsharing/error_page.html', {'text': 'Queried Data Object Could Not Be Found'}, context_instance=RequestContext(request))
    try:
        consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer)
        request_url = TWITTER_SEARCH_URL + data.url
        resp, cont = client.request(request_url, 'GET')
        if resp['status'] == '200':
            new_dic = ast.literal_eval(cont)
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
        content = urllib.urlopen("http://api.pinterest.com/v1/urls/count.json?callback=&url=" + data.url).read()
        new_dic = ast.literal_eval(content)
        data.pins = int(new_dic['count'])
        data.save()
    except Exception as e:
        print "Pinterest Failure"
        print e
    try:
        content = urllib.urlopen("http://www.linkedin.com/countserv/count/share?url=" + data.url + "&format=json").read()
        new_dic = ast.literal_eval(content)
        data.linkedin = int(new_dic['count'])
        data.save()
    except Exception as e:
        print "LinkedIn Failure"
        print e
    try:
        request_url = "https://plusone.google.com/u/0/_/+1/fastbutton?url=" + convertString(data.url)
        content = urllib.urlopen(request_url).read()
        point = 1400
        searching = True
        while(point < 1800 and searching):
            if content[point:point+19] == "window.__SSR = {c: ":
                count = 0
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
        if checkForYouTube(data_id):
            my_url = STATISTICS_URL + "?id=" + getVideoID(data.url) + "&part=statistics&field=monetizationDetails" + "%" + "2Cstatistics&key=" + API_KEY
            r = urllib2.urlopen(my_url)
            response = ast.literal_eval(r.read())
            print response['items'][0]['snippet']['title']
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


def getTwitterStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer)
        request_url = TWITTER_SEARCH_URL + data.url
        resp, cont = client.request(request_url, 'GET')     # Request total # of tweets that contain url (or keyword)
        if resp['status'] == '200':
            new_dic = ast.literal_eval(cont)                # If request is received correctly, save tweet information
            data.tweets = int(new_dic['count'])
            data.save()
        else:
            print "Twitter API call failed"
        tweets_url = "https://api.twitter.com/1.1/search/tweets.json?q=%" + data.url + "&count=10"
        resp, cont = client.request(tweets_url, 'GET')
    except Exception as e:
        print e
    return redirect('fbsharing.views.getStumbledUponStats', data_id)


def getRecentTweets(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        results = api.search(q=data.url)
        for result in results:
            print result.text
    except Exception as e:
        print e
    return redirect('fbsharing.views.displayStats', data_id)


def getStumbledUponStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        content = urllib.urlopen("http://www.stumbleupon.com/services/1.01/badge.getinfo?url=" + data.url)
        cont_data = json.load(content)
        if cont_data['result']['in_index'] == False:
            data.stumble = 0
        else:
            data.stumble = int(cont_data['result']['views'])
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.getPinterestStats', data_id)


def getPinterestStats(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        content = urllib.urlopen("http://api.pinterest.com/v1/urls/count.json?callback=&url=" + data.url).read()
        new_dic = ast.literal_eval(content)
        data.pins = int(new_dic['count'])
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.getLinkedInShares', data_id)


def getLinkedInShares(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        content = urllib.urlopen("http://www.linkedin.com/countserv/count/share?url=" + data.url + "&format=json").read()
        new_dic = ast.literal_eval(content)
        data.linkedin = int(new_dic['count'])
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.getGPlusOnes', data_id)


def getGPlusOnes(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        request_url = GOOG_ACT_SEARCH + "?query=" + convertString(data.url) + "&key=" + API_KEY
        content = urllib.urlopen(request_url).read()
        new_dic = ast.literal_eval(content)
        for item in new_dic['items']:
            if makeHttp(data_id) == item['object']['attachments'][0]['url']:
                activity_id = item['id']
                request_url2 = GOOG_ACT_SEARCH + "/" + activity_id + "?key=" + API_KEY
                content2 = urllib.urlopen(request_url2).read()
                dic = ast.literal_eval(content2)
                data.g_reshares = int(dic['object']['resharers']['totalItems'])
                data.g_plus_one = int(dic['object']['plusoners']['totalItems'])
                data.g_replies = int(dic['object']['replies']['totalItems'])
                data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.oneTimeYouTubeStats', data_id)


def socialShares(request, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
        sharedcount_data_url = "http://api.sharedcount.com/?url=" + data.url
        result = urllib2.urlopen(sharedcount_data_url)
        shared_result = json.load(result)
        # Recording the change in share count numbers since the previous run
        data.facebook_total = int(shared_result["Facebook"]["total_count"]) - data.campaign.facebook_total
        data.facebook_shares = int(shared_result["Facebook"]["share_count"]) - data.campaign.facebook_shares
        data.facebook_likes = int(shared_result["Facebook"]["like_count"]) - data.campaign.facebook_likes
        data.facebook_comments = int(shared_result["Facebook"]["comment_count"]) - data.campaign.facebook_comments
        data.tweets = int(shared_result["Twitter"]) - data.campaign.tweets
        data.g_plus_one = int(shared_result["GooglePlusOne"]) - data.campaign.g_plus_one
        data.pins = int(shared_result["Pinterest"]) - data.campaign.pins
        data.linkedin = int(shared_result["LinkedIn"]) - data.campaign.linkedin
        data.stumble = int(shared_result["StumbleUpon"]) - data.campaign.stumble
        data.diggs = int(shared_result["Diggs"]) - data.campaign.diggs

        # Recording total share count numbers for the campaign
        data.campaign.facebook_total = int(shared_result["Facebook"]["total_count"])
        data.campaign.facebook_shares = int(shared_result["Facebook"]["share_count"])
        data.campaign.facebook_likes = int(shared_result["Facebook"]["like_count"])
        data.campaign.facebook_comments = int(shared_result["Facebook"]["comment_count"])
        data.campaign.tweets = int(shared_result["Twitter"])
        data.campaign.g_plus_one = int(shared_result["GooglePlusOne"])
        data.campaign.pins = int(shared_result["Pinterest"])
        data.campaign.linkedin = int(shared_result["LinkedIn"])
        data.campaign.stumble = int(shared_result["StumbleUpon"])
        data.campaign.diggs = int(shared_result["Diggs"])

        data.campaign.save()
        data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.youtube', data_id)


def youtube(request, data_id):
    if checkForYouTube(data_id):
        try:
            myData = fbDataRequest.objects.get(pk=data_id)
            my_url = STATISTICS_URL + "?id=" + getVideoID(myData.url) + "&part=statistics&field=monetizationDetails%" + "2Cstatistics&key=" + API_KEY
            r = urllib2.urlopen(my_url)
            response = ast.literal_eval(r.read())
            print response
            # Recording the change in youtube metrics since last run
            myData.yt_comment_count = int(response['items'][0]['statistics']['commentCount']) - myData.campaign.yt_comment_count
            myData.yt_view_count = int(response['items'][0]['statistics']['viewCount']) - myData.campaign.yt_view_count
            myData.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount']) - myData.campaign.yt_fav_count
            myData.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount']) - myData.campaign.yt_dislike_count
            myData.yt_like_count = int(response['items'][0]['statistics']['likeCount']) - myData.campaign.yt_like_count
            # Recording total youtube metric numbers for campaign
            myData.campaign.yt_comment_count = int(response['items'][0]['statistics']['commentCount'])
            myData.campaign.yt_view_count = int(response['items'][0]['statistics']['viewCount'])
            myData.campaign.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount'])
            myData.campaign.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount'])
            myData.campaign.yt_like_count = int(response['items'][0]['statistics']['likeCount'])
            # Saving Data
            myData.campaign.save()
            myData.save()
        except Exception as e:
            print e
    return redirect('fbsharing.views.viewCampaign', myData.id)


def oneTimeYouTubeStats(request, data_id):
    if checkForYouTube(data_id):
        try:
            data = fbDataRequest.objects.get(pk=data_id)
            my_url = STATISTICS_URL + "?id=" + getVideoID(data.url) + "&part=statistics&field=monetizationDetails" + "%" + "2Cstatistics&key=" + API_KEY
            r = urllib2.urlopen(my_url)
            response = ast.literal_eval(r.read())
            data.yt_comment_count = int(response['items'][0]['statistics']['commentCount'])
            data.yt_view_count = int(response['items'][0]['statistics']['viewCount'])
            data.yt_fav_count = int(response['items'][0]['statistics']['favoriteCount'])
            data.yt_dislike_count = int(response['items'][0]['statistics']['dislikeCount'])
            data.yt_like_count = int(response['items'][0]['statistics']['likeCount'])
            data.save(0)
        except Exception as e:
            print e
    return redirect('fbsharing.views.displayStats', data_id)


def updateAllCampaigns(request):
    try:
        campaigns = Campaign.objects.filter(current=True)
        # Update all engagement statistics for each current campaign
        for campaign in campaigns:
            daily_data = fbDataRequest(url=campaign.url, campaign=campaign)
            daily_data.save()
            socialShares(daily_data.id)
            youtube(daily_data.id)
    except Exception as e:
        raise e
    return render_to_response('fbsharing/view_campaigns.html', {'campaigns': campaigns}, context_instance=RequestContext(request))


def addCampaign(request):
    campaign = Campaign()
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            campaign = form.save()
            return redirect('fbsharing.views.initializeCampaign', campaign.id)
    else:
        form = CampaignForm(instance=campaign)
    return render_to_response('fbsharing/new_campaign.html', {'form': form, 'campaign': campaign}, context_instance=RequestContext(request))


def initializeCampaign(request, campaign_id):
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
        campaign.facebook_comments = 0
        campaign.facebook_likes = 0
        campaign.facebook_shares = 0
        campaign.facebook_total = 0
        campaign.yt_like_count = 0
        campaign.yt_dislike_count = 0
        campaign.yt_fav_count = 0
        campaign.yt_comment_count = 0
        campaign.yt_view_count = 0
        campaign.tweets = 0
        campaign.g_plus_one = 0
        campaign.g_replies = 0
        campaign.g_reshares = 0
        campaign.linkedin = 0
        campaign.stumble = 0
        campaign.pins = 0
        campaign.diggs = 0
        campaign.save()
        daily_data = fbDataRequest(url=campaign.url, campaign=campaign)
        daily_data.save()
    except Exception as e:
        print e
    return redirect('fbsharing.views.socialShares', daily_data.id)
    


def viewCampaign(request, data_id):
    try:
        daily_data = fbDataRequest.objects.get(pk=data_id)
        campaign = daily_data.campaign
    except Exception as e:
        print e
    return render_to_response('fbsharing/view_campaign_data.html', {'campaign': campaign, 'dailly_data': daily_data}, context_instance=RequestContext(request))


def compareCampaigns(request, campaign_1, campaign_2):
    try:
        campaign_1 = Campaign.objects.get(pk=campaign_1)
        campaign_2 = Campaign.objects.get(pk=campaign_2)
    except Exception as e:
        print "could not find campaigns"
        return render_to_response('fbsharing/error_page', {'text': 'One or more of the campaigns requested cannot be displayed'}, context_instance=RequestContext(request))
    return render_to_response('fbsharing/compare_campaign.html', {'campaign_1': campaign_1, 'campaign_2': campaign_2}, context_instance=RequestContext(request))


def removeAllTags(request):
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/fb/tagRemover/' + str(facebook.id)
    return HttpResponseRedirect(REQUEST_TOKEN_URL + '?client_id=%s&client_secret=%s&grant_type=client_credentials&redirect_uri=%s' % (APP_ID, APP_SECRET, callback_url))


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


def ripVidIDFromChannelFeed(feed_url):
    o = urlparse.urlparse(feed_url)
    return o.path[18:]


def findActivity(my_dict, data_id):
    try:
        data = fbDataRequest.objects.get(pk=data_id)
    except Exception, e:
        raise e
    if data.url[:4]!='http':
        target = 'https://' + data.url[6:]
    elif data.url[:7]=='http://':
        target = 'https://' + data.url[7:]
    else:
        target = data.url
    for item in my_dict['items']:
        print item['object']['plusoners']
        if item['object'].has_key('attachments'):
            #print item['object']['attachments'][0]['url']
            print item['id']
            if target == item['object']['attachments'][0]['url'][0:len(target)] or True:
                print 'FOUND IT'
                activity_id = item['id']
                request_url2 = GOOG_ACT_SEARCH + "/" + activity_id + "?key=" + API_KEY
                content2 = urllib.urlopen(request_url2).read()
                dic = ast.literal_eval(content2)
                if dic['object'].has_key('plusoners'):
                    print "KEY FOUND"
                    data.g_reshares = int(dic['object']['resharers']['totalItems']) + data.g_reshares
                    data.g_plus_one = int(dic['object']['plusoners']['totalItems']) + data.g_plus_one
                    data.g_replies = int(dic['object']['replies']['totalItems']) + data.g_replies
                    data.save()
                    print data.g_plus_one
                '''
                data.g_reshares = int(dic['object']['resharers']['totalItems']) - campaign.g_reshares
                data.g_plus_one = int(dic['object']['plusoners']['totalItems']) - campaign.g_plus_one
                data.g_replies = int(dic['object']['replies']['totalItems']) - campaign.g_replies
                campaign.g_reshares = int(dic['object']['resharers']['totalItems'])
                campaign.g_plus_one = int(dic['object']['plusoners']['totalItems'])
                campaign.g_replies = int(dic['object']['replies']['totalItems'])
                '''
                #return True
    return False
