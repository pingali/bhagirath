# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Master_BackgroundTask'
        db.delete_table('translation_master_backgroundtask')

        # Deleting model 'Leaderboard'
        db.delete_table('translation_leaderboard')

        # Adding model 'Master_English2Hindi'
        db.create_table('translation_master_english2hindi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('english_word', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2000)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('hindi_word', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('translation', ['Master_English2Hindi'])

        # Adding model 'WeeklyLeaderboard'
        db.create_table('translation_weeklyleaderboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('points_earned_this_week', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('translation', ['WeeklyLeaderboard'])

        # Adding model 'OverallLeaderboard'
        db.create_table('translation_overallleaderboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('overall_points_earned', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('translation', ['OverallLeaderboard'])

        # Deleting field 'UserProfile.city'
        db.delete_column('translation_userprofile', 'city')

        # Adding field 'UserProfile.state'
        db.add_column('translation_userprofile', 'state', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['translation.Master_GeographicalRegion'], null=True), keep_default=False)

        # Adding field 'UserProfile.overall_score'
        db.add_column('translation_userprofile', 'overall_score', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.prev_week_score'
        db.add_column('translation_userprofile', 'prev_week_score', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.total_translated_sentences'
        db.add_column('translation_userprofile', 'total_translated_sentences', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.total_evaluated_sentences'
        db.add_column('translation_userprofile', 'total_evaluated_sentences', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.total_uploaded_tasks'
        db.add_column('translation_userprofile', 'total_uploaded_tasks', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'StatCounter.created_on'
        db.add_column('translation_statcounter', 'created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 30, 23, 28, 12, 706645)), keep_default=False)

        # Deleting field 'StaticMicrotask.google_translation'
        db.delete_column('translation_staticmicrotask', 'google_translation')

        # Adding field 'StaticMicrotask.machine_translation'
        db.add_column('translation_staticmicrotask', 'machine_translation', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True), keep_default=False)

        # Deleting field 'TransactionAction.microtask'
        db.delete_column('translation_transactionaction', 'microtask_id')

        # Adding field 'TransactionAction.static_microtask'
        db.add_column('translation_transactionaction', 'static_microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.StaticMicrotask'], null=True), keep_default=False)

        # Adding field 'TransactionAction.action_timestamp'
        db.add_column('translation_transactionaction', 'action_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 30, 23, 28, 27, 508366)), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Master_BackgroundTask'
        db.create_table('translation_master_backgroundtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trigger_frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('bg_task_name', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('translation', ['Master_BackgroundTask'])

        # Adding model 'Leaderboard'
        db.create_table('translation_leaderboard', (
            ('points_earned_this_week', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('overall_points_earned', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('translation', ['Leaderboard'])

        # Deleting model 'Master_English2Hindi'
        db.delete_table('translation_master_english2hindi')

        # Deleting model 'WeeklyLeaderboard'
        db.delete_table('translation_weeklyleaderboard')

        # Deleting model 'OverallLeaderboard'
        db.delete_table('translation_overallleaderboard')

        # Adding field 'UserProfile.city'
        db.add_column('translation_userprofile', 'city', self.gf('django.db.models.fields.CharField')(default=None, max_length=50), keep_default=False)

        # Deleting field 'UserProfile.state'
        db.delete_column('translation_userprofile', 'state_id')

        # Deleting field 'UserProfile.overall_score'
        db.delete_column('translation_userprofile', 'overall_score')

        # Deleting field 'UserProfile.prev_week_score'
        db.delete_column('translation_userprofile', 'prev_week_score')

        # Deleting field 'UserProfile.total_translated_sentences'
        db.delete_column('translation_userprofile', 'total_translated_sentences')

        # Deleting field 'UserProfile.total_evaluated_sentences'
        db.delete_column('translation_userprofile', 'total_evaluated_sentences')

        # Deleting field 'UserProfile.total_uploaded_tasks'
        db.delete_column('translation_userprofile', 'total_uploaded_tasks')

        # Deleting field 'StatCounter.created_on'
        db.delete_column('translation_statcounter', 'created_on')

        # Adding field 'StaticMicrotask.google_translation'
        db.add_column('translation_staticmicrotask', 'google_translation', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True), keep_default=False)

        # Deleting field 'StaticMicrotask.machine_translation'
        db.delete_column('translation_staticmicrotask', 'machine_translation')

        # Adding field 'TransactionAction.microtask'
        db.add_column('translation_transactionaction', 'microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.StaticMicrotask'], null=True), keep_default=False)

        # Deleting field 'TransactionAction.static_microtask'
        db.delete_column('translation_transactionaction', 'static_microtask_id')

        # Deleting field 'TransactionAction.action_timestamp'
        db.delete_column('translation_transactionaction', 'action_timestamp')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'translation.master_action': {
            'Meta': {'object_name': 'Master_Action'},
            'action': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_agegroup': {
            'Meta': {'object_name': 'Master_AgeGroup'},
            'age_group_tag': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_age': ('django.db.models.fields.IntegerField', [], {}),
            'minimum_age': ('django.db.models.fields.IntegerField', [], {})
        },
        'translation.master_english2hindi': {
            'Meta': {'object_name': 'Master_English2Hindi'},
            'english_word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'}),
            'hindi_word': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'translation.master_geographicalregion': {
            'Meta': {'object_name': 'Master_GeographicalRegion'},
            'geographical_region': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_hindiwords': {
            'Meta': {'object_name': 'Master_HindiWords'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'transliterated': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        'translation.master_interesttags': {
            'Meta': {'object_name': 'Master_InterestTags'},
            'category': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'need_evaluation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'translation.master_language': {
            'Meta': {'object_name': 'Master_Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'translation.master_rank': {
            'Meta': {'object_name': 'Master_Rank'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentile': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'translation.master_role': {
            'Meta': {'object_name': 'Master_Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'role_condition': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'translation.microtask': {
            'Meta': {'object_name': 'Microtask'},
            'assign_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']"}),
            'subtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Subtask']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"})
        },
        'translation.overallleaderboard': {
            'Meta': {'object_name': 'OverallLeaderboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_points_earned': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'logout_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.statcounter': {
            'Meta': {'object_name': 'StatCounter'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_articles': ('django.db.models.fields.IntegerField', [], {}),
            'registered_users': ('django.db.models.fields.IntegerField', [], {}),
            'translated_sentences': ('django.db.models.fields.IntegerField', [], {})
        },
        'translation.staticmicrotask': {
            'Meta': {'object_name': 'StaticMicrotask'},
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hop_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_translation': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'scoring_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stability': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'subtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Subtask']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'translated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'transliterated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        'translation.subtask': {
            'Meta': {'object_name': 'Subtask'},
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_average_stability': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_data': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'translated_data': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        'translation.task': {
            'Meta': {'ordering': "['time_to_publish']", 'object_name': 'Task'},
            'age_group_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_AgeGroup']", 'null': 'True'}),
            'budget': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'}),
            'context_size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dampening_factor': ('django.db.models.fields.FloatField', [], {'default': '0.5', 'null': 'True'}),
            'geographical_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_GeographicalRegion']", 'null': 'True'}),
            'html_doc_content': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'html_doc_name': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['translation.Master_InterestTags']", 'null': 'True', 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_language'", 'to': "orm['translation.Master_Language']"}),
            'target_language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_language'", 'to': "orm['translation.Master_Language']"}),
            'time_to_publish': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'upload_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.transactionaction': {
            'Meta': {'object_name': 'TransactionAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Action']"}),
            'action_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Session']"}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']", 'null': 'True'}),
            'subtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Subtask']", 'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.userhistory': {
            'Meta': {'object_name': 'UserHistory'},
            'assign_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'change_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_active_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'microtask': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Microtask']", 'null': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'reputation_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'stability': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']"}),
            'status_flag': ('django.db.models.fields.CharField', [], {'default': "'Raw'", 'max_length': '10'}),
            'submission_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Subtask']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'time_to_live': ('django.db.models.fields.FloatField', [], {'default': '100000.0', 'null': 'True'}),
            'translated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'transliterated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'evaluator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_InterestTags']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_Language']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'overall_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'prev_week_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Rank']", 'null': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Master_GeographicalRegion']", 'null': 'True'}),
            'total_evaluated_sentences': ('django.db.models.fields.IntegerField', [], {}),
            'total_translated_sentences': ('django.db.models.fields.IntegerField', [], {}),
            'total_uploaded_tasks': ('django.db.models.fields.IntegerField', [], {}),
            'translator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'translation.weeklyleaderboard': {
            'Meta': {'object_name': 'WeeklyLeaderboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned_this_week': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['translation']
