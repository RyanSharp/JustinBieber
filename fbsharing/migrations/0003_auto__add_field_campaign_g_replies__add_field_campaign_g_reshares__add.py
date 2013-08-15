# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Campaign.g_replies'
        db.add_column(u'fbsharing_campaign', 'g_replies',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Campaign.g_reshares'
        db.add_column(u'fbsharing_campaign', 'g_reshares',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'fbDataRequest.g_replies'
        db.add_column(u'fbsharing_fbdatarequest', 'g_replies',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'fbDataRequest.g_reshares'
        db.add_column(u'fbsharing_fbdatarequest', 'g_reshares',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Campaign.g_replies'
        db.delete_column(u'fbsharing_campaign', 'g_replies')

        # Deleting field 'Campaign.g_reshares'
        db.delete_column(u'fbsharing_campaign', 'g_reshares')

        # Deleting field 'fbDataRequest.g_replies'
        db.delete_column(u'fbsharing_fbdatarequest', 'g_replies')

        # Deleting field 'fbDataRequest.g_reshares'
        db.delete_column(u'fbsharing_fbdatarequest', 'g_reshares')


    models = {
        u'fbsharing.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'current': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'diggs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_comments': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_likes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_plus_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_replies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_reshares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'stumble': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tweets': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'yt_comment_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_dislike_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_fav_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_like_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_view_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'fbsharing.fbdatarequest': {
            'Meta': {'object_name': 'fbDataRequest'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbsharing.Campaign']", 'null': 'True', 'blank': 'True'}),
            'diggs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_comments': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_likes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_plus_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_replies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'g_reshares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stumble': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tweets': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'yt_comment_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_dislike_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_fav_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_like_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yt_view_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fbsharing']