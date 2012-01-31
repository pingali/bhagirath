# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Master_HindiWords'
        db.create_table('translation_master_hindiwords', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2000)),
            ('transliterated', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('translation', ['Master_HindiWords'])

        # Adding model 'Master_AgeGroup'
        db.create_table('translation_master_agegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age_group_tag', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('minimum_age', self.gf('django.db.models.fields.IntegerField')()),
            ('maximum_age', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('translation', ['Master_AgeGroup'])

        # Adding model 'Master_GeographicalRegion'
        db.create_table('translation_master_geographicalregion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geographical_region', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('translation', ['Master_GeographicalRegion'])

        # Adding model 'Master_InterestTags'
        db.create_table('translation_master_interesttags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('need_evaluation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('translation', ['Master_InterestTags'])

        # Adding model 'Master_Action'
        db.create_table('translation_master_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('translation', ['Master_Action'])

        # Adding model 'Master_Role'
        db.create_table('translation_master_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('role_condition', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('translation', ['Master_Role'])

        # Adding model 'Master_Rank'
        db.create_table('translation_master_rank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('percentile', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('translation', ['Master_Rank'])

        # Adding model 'Master_BackgroundTask'
        db.create_table('translation_master_backgroundtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bg_task_name', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('trigger_frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('translation', ['Master_BackgroundTask'])

        # Adding model 'Master_Language'
        db.create_table('translation_master_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('region', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('translation', ['Master_Language'])

        # Adding model 'StatCounter'
        db.create_table('translation_statcounter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registered_users', self.gf('django.db.models.fields.IntegerField')()),
            ('translated_sentences', self.gf('django.db.models.fields.IntegerField')()),
            ('published_articles', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('translation', ['StatCounter'])

        # Adding model 'Leaderboard'
        db.create_table('translation_leaderboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('points_earned_this_week', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('overall_points_earned', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('translation', ['Leaderboard'])

        # Adding model 'UserProfile'
        db.create_table('translation_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('translator', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('contributor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('evaluator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Master_Rank'], null=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
        ))
        db.send_create_signal('translation', ['UserProfile'])

        # Adding M2M table for field language on 'UserProfile'
        db.create_table('translation_userprofile_language', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['translation.userprofile'], null=False)),
            ('master_language', models.ForeignKey(orm['translation.master_language'], null=False))
        ))
        db.create_unique('translation_userprofile_language', ['userprofile_id', 'master_language_id'])

        # Adding M2M table for field interests on 'UserProfile'
        db.create_table('translation_userprofile_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['translation.userprofile'], null=False)),
            ('master_interesttags', models.ForeignKey(orm['translation.master_interesttags'], null=False))
        ))
        db.create_unique('translation_userprofile_interests', ['userprofile_id', 'master_interesttags_id'])

        # Adding model 'Session'
        db.create_table('translation_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('login_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('logout_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('translation', ['Session'])

        # Adding model 'Task'
        db.create_table('translation_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_doc_name', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('html_doc_content', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('upload_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('time_to_publish', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('source_language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source_language', to=orm['translation.Master_Language'])),
            ('target_language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_language', to=orm['translation.Master_Language'])),
            ('context_size', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('budget', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True)),
            ('dampening_factor', self.gf('django.db.models.fields.FloatField')(default=0.5, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('age_group_tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Master_AgeGroup'], null=True)),
            ('geographical_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Master_GeographicalRegion'], null=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('translation', ['Task'])

        # Adding M2M table for field interest_tags on 'Task'
        db.create_table('translation_task_interest_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['translation.task'], null=False)),
            ('master_interesttags', models.ForeignKey(orm['translation.master_interesttags'], null=False))
        ))
        db.create_unique('translation_task_interest_tags', ['task_id', 'master_interesttags_id'])

        # Adding model 'Subtask'
        db.create_table('translation_subtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Task'])),
            ('original_data', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('translated_data', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('current_average_stability', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('assigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('translation', ['Subtask'])

        # Adding model 'StaticMicrotask'
        db.create_table('translation_staticmicrotask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Task'])),
            ('subtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Subtask'])),
            ('original_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('translated_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('transliterated_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('google_translation', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('assigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stability', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('scoring_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hop_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('translation', ['StaticMicrotask'])

        # Adding model 'Microtask'
        db.create_table('translation_microtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Task'])),
            ('subtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Subtask'])),
            ('static_microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.StaticMicrotask'])),
            ('original_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('assign_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('assigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('translation', ['Microtask'])

        # Adding model 'TransactionAction'
        db.create_table('translation_transactionaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Session'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Master_Action'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Task'])),
            ('subtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Subtask'], null=True)),
            ('microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.StaticMicrotask'], null=True)),
        ))
        db.send_create_signal('translation', ['TransactionAction'])

        # Adding model 'UserHistory'
        db.create_table('translation_userhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Task'])),
            ('subtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Subtask'])),
            ('static_microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.StaticMicrotask'])),
            ('microtask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['translation.Microtask'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('original_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('transliterated_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('translated_sentence', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('assign_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('submission_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('reputation_score', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('stability', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('change_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_to_live', self.gf('django.db.models.fields.FloatField')(default=100000.0, null=True)),
            ('status_flag', self.gf('django.db.models.fields.CharField')(default='Raw', max_length=10)),
            ('current_active_tag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('translation', ['UserHistory'])


    def backwards(self, orm):
        
        # Deleting model 'Master_HindiWords'
        db.delete_table('translation_master_hindiwords')

        # Deleting model 'Master_AgeGroup'
        db.delete_table('translation_master_agegroup')

        # Deleting model 'Master_GeographicalRegion'
        db.delete_table('translation_master_geographicalregion')

        # Deleting model 'Master_InterestTags'
        db.delete_table('translation_master_interesttags')

        # Deleting model 'Master_Action'
        db.delete_table('translation_master_action')

        # Deleting model 'Master_Role'
        db.delete_table('translation_master_role')

        # Deleting model 'Master_Rank'
        db.delete_table('translation_master_rank')

        # Deleting model 'Master_BackgroundTask'
        db.delete_table('translation_master_backgroundtask')

        # Deleting model 'Master_Language'
        db.delete_table('translation_master_language')

        # Deleting model 'StatCounter'
        db.delete_table('translation_statcounter')

        # Deleting model 'Leaderboard'
        db.delete_table('translation_leaderboard')

        # Deleting model 'UserProfile'
        db.delete_table('translation_userprofile')

        # Removing M2M table for field language on 'UserProfile'
        db.delete_table('translation_userprofile_language')

        # Removing M2M table for field interests on 'UserProfile'
        db.delete_table('translation_userprofile_interests')

        # Deleting model 'Session'
        db.delete_table('translation_session')

        # Deleting model 'Task'
        db.delete_table('translation_task')

        # Removing M2M table for field interest_tags on 'Task'
        db.delete_table('translation_task_interest_tags')

        # Deleting model 'Subtask'
        db.delete_table('translation_subtask')

        # Deleting model 'StaticMicrotask'
        db.delete_table('translation_staticmicrotask')

        # Deleting model 'Microtask'
        db.delete_table('translation_microtask')

        # Deleting model 'TransactionAction'
        db.delete_table('translation_transactionaction')

        # Deleting model 'UserHistory'
        db.delete_table('translation_userhistory')


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
        'translation.leaderboard': {
            'Meta': {'object_name': 'Leaderboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_points_earned': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'points_earned_this_week': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        'translation.master_backgroundtask': {
            'Meta': {'object_name': 'Master_BackgroundTask'},
            'bg_task_name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trigger_frequency': ('django.db.models.fields.IntegerField', [], {})
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
        'translation.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'logout_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'translation.statcounter': {
            'Meta': {'object_name': 'StatCounter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_articles': ('django.db.models.fields.IntegerField', [], {}),
            'registered_users': ('django.db.models.fields.IntegerField', [], {}),
            'translated_sentences': ('django.db.models.fields.IntegerField', [], {})
        },
        'translation.staticmicrotask': {
            'Meta': {'object_name': 'StaticMicrotask'},
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_translation': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'hop_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']", 'null': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Session']"}),
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
            'microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Microtask']", 'null': 'True'}),
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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'evaluator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_InterestTags']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_Language']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Rank']", 'null': 'True'}),
            'translator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['translation']
