from django.db import models

# Create your models here.

# This model is used to run the campaign.  All values for sharing data are cummulative for total campaign
class Campaign(models.Model):
    url = models.CharField(max_length=255)
    end_date = models.DateField(blank=True, null=True)
    current = models.NullBooleanField(default=True, blank=True, null=True)
    start_date = models.DateField(auto_now=True)
    facebook_total = models.IntegerField(blank=True, null=True)
    facebook_shares = models.IntegerField(blank=True, null=True)
    facebook_likes = models.IntegerField(blank=True, null=True)
    facebook_comments = models.IntegerField(blank=True, null=True)
    tweets = models.IntegerField(blank=True, null=True)
    stumble = models.IntegerField(blank=True, null=True)
    pins = models.IntegerField(blank=True, null=True)
    g_plus_one = models.IntegerField(blank=True, null=True)
    g_replies = models.IntegerField(blank=True, null=True)
    g_reshares = models.IntegerField(blank=True, null=True)
    linkedin = models.IntegerField(blank=True, null=True)
    diggs = models.IntegerField(blank=True, null=True)
    yt_comment_count = models.IntegerField(blank=True, null=True)
    yt_view_count = models.IntegerField(blank=True, null=True)
    yt_fav_count = models.IntegerField(blank=True, null=True)
    yt_dislike_count = models.IntegerField(blank=True, null=True)
    yt_like_count = models.IntegerField(blank=True, null=True)


# This model holds the change per day.  A new model is created for each day of the campaign with the sharing data being the change fromt he previous day
class fbDataRequest(models.Model):
    campaign = models.ForeignKey(Campaign, blank=True, null=True)
    timestamp = models.DateField(auto_now=True)
    url = models.CharField(max_length=255)
    facebook_total = models.IntegerField(blank=True, null=True)
    facebook_shares = models.IntegerField(blank=True, null=True)
    facebook_likes = models.IntegerField(blank=True, null=True)
    facebook_comments = models.IntegerField(blank=True, null=True)
    tweets = models.IntegerField(blank=True, null=True)
    stumble = models.IntegerField(blank=True, null=True)
    pins = models.IntegerField(blank=True, null=True)
    g_plus_one = models.IntegerField(blank=True, null=True)
    g_replies = models.IntegerField(blank=True, null=True)
    g_reshares = models.IntegerField(blank=True, null=True)
    linkedin = models.IntegerField(blank=True, null=True)
    diggs = models.IntegerField(blank=True, null=True)
    yt_comment_count = models.IntegerField(blank=True, null=True)
    yt_view_count = models.IntegerField(blank=True, null=True)
    yt_fav_count = models.IntegerField(blank=True, null=True)
    yt_dislike_count = models.IntegerField(blank=True, null=True)
    yt_like_count = models.IntegerField(blank=True, null=True)


class DailyRun(models.Model):
    pending = models.CommaSeparatedIntegerField(max_length=255, blank=True, null=True)
    completed = models.CommaSeparatedIntegerField(max_length=255, blank=True, null=True)
    more = models.NullBooleanField(blank=True, null=True)
    current = models.ForeignKey(fbDataRequest, blank=True, null=True)
