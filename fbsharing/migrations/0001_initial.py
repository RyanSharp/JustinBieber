# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Campaign'
        db.create_table(u'fbsharing_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('current', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('facebook_total', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_shares', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_likes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_comments', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tweets', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stumble', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pins', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('g_plus_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('linkedin', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('diggs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_comment_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_view_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_fav_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_dislike_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_like_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fbsharing', ['Campaign'])

        # Adding model 'fbDataRequest'
        db.create_table(u'fbsharing_fbdatarequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fbsharing.Campaign'])),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('facebook_total', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_shares', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_likes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('facebook_comments', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tweets', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stumble', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pins', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('g_plus_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('linkedin', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('diggs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_comment_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_view_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_fav_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_dislike_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yt_like_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fbsharing', ['fbDataRequest'])


    def backwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table(u'fbsharing_campaign')

        # Deleting model 'fbDataRequest'
        db.delete_table(u'fbsharing_fbdatarequest')


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
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fbsharing.Campaign']"}),
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