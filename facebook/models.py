from django.db import models

# Create your models here.
class FacebookUser(models.Model):
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	user_id = models.CharField(max_length=255)
	name = models.CharField(max_length=255)


class PublicPost(models.Model):
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	post_id = models.CharField(max_length=255)
	from_user = models.ForeignKey(FacebookUser)
	message = models.TextField()
	included_url = models.URLField(null=True, blank=True)
	url_name = models.CharField(max_length=255, null=True, blank=True)
	url_caption = models.CharField(max_length=255, null=True, blank=True)
	url_description = models.CharField(max_length=255, null=True, blank=True)
	url_picture = models.URLField(null=True, blank=True)
	url_video = models.URLField(null=True, blank=True)
	url_properties = models.CharField(max_length=255, null=True, blank=True)
	icon = models.CharField(max_length=255)
	post_type = models.CharField(max_length=255)
	place_id = models.CharField(max_length=255, null=True, blank=True)
	shares = models.IntegerField()
	status_type = models.CharField(max_length=40)


class PostTarget(models.Model):
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	post = models.ForeignKey(PublicPost)
	user_id = models.CharField(max_length=255)
	name = models.CharField(max_length=255)


class PostComment(models.Model):
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	post = models.ForeignKey(PublicPost)
	from_id = models.CharField(max_length=255)
	message = models.CharField(max_length=255)
	comment_id = models.CharField(max_length=255)
