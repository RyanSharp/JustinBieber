# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'fbDataRequest.campaign'
        db.alter_column(u'fbsharing_fbdatarequest', 'campaign_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbsharing.Campaign'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'fbDataRequest.campaign'
        raise RuntimeError("Cannot reverse this migration. 'fbDataRequest.campaign' and its values cannot be restored.")

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