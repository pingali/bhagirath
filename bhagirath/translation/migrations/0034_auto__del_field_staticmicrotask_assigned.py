# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'StaticMicrotask.assigned'
        db.delete_column('translation_staticmicrotask', 'assigned')


    def backwards(self, orm):
        
        # Adding field 'StaticMicrotask.assigned'
        db.add_column('translation_staticmicrotask', 'assigned', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


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
        'translation.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {})
        },
        'translation.master_action': {
            'Meta': {'ordering': "['action']", 'object_name': 'Master_Action'},
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
        'translation.master_educationdomain': {
            'Meta': {'ordering': "['domain']", 'object_name': 'Master_EducationDomain'},
            'domain': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_educationqualification': {
            'Meta': {'ordering': "['education_qualification']", 'object_name': 'Master_EducationQualification'},
            'education_qualification': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_english2hindi': {
            'Meta': {'ordering': "['english_word']", 'object_name': 'Master_English2Hindi'},
            'english_word': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'hindi_word': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'translation.master_experiment': {
            'Meta': {'object_name': 'Master_Experiment'},
            'bit_array': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_geographicalregion': {
            'Meta': {'ordering': "['geographical_region']", 'object_name': 'Master_GeographicalRegion'},
            'geographical_region': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'translation.master_hindiwords': {
            'Meta': {'ordering': "['original']", 'object_name': 'Master_HindiWords'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'translation.master_interesttags': {
            'Meta': {'ordering': "['category']", 'object_name': 'Master_InterestTags'},
            'category': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'need_evaluation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'translation.master_language': {
            'Meta': {'ordering': "['language']", 'object_name': 'Master_Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'translation.master_languageexpertise': {
            'Meta': {'ordering': "['language']", 'object_name': 'Master_LanguageExpertise'},
            'expertise': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Language']"})
        },
        'translation.master_rank': {
            'Meta': {'object_name': 'Master_Rank'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentile': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'translation.master_role': {
            'Meta': {'ordering': "['role']", 'object_name': 'Master_Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'role_condition': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'translation.master_sampletranslations': {
            'Meta': {'object_name': 'Master_SampleTranslations'},
            'google_translation': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_sentence': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'user_translation': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'translation.microtask': {
            'Meta': {'object_name': 'Microtask'},
            'assign_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"})
        },
        'translation.overallleaderboard': {
            'Meta': {'object_name': 'OverallLeaderboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_points_earned': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'translation.reviseduserhistory': {
            'Meta': {'object_name': 'RevisedUserHistory'},
            'assign_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'correction_episode': ('jsonfield.fields.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'reputation_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']"}),
            'submission_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'translated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'translation.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'logout_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
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
            'bit_array': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Experiment']", 'null': 'True'}),
            'hop_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_translation': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'meaning': ('jsonfield.fields.JSONField', [], {}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'scoring_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stability': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'status_flag': ('django.db.models.fields.CharField', [], {'default': "'Circulate'", 'max_length': '10'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'translated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'translation_requests_sent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'translations_received': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
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
            'parsed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_language'", 'to': "orm['translation.Master_Language']"}),
            'target_language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_language'", 'to': "orm['translation.Master_Language']"}),
            'time_to_publish': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'upload_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'translation.transactionaction': {
            'Meta': {'object_name': 'TransactionAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Action']"}),
            'action_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Session']"}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']", 'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'translation.userhistory': {
            'Meta': {'object_name': 'UserHistory'},
            'assign_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'change_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'correction_episode': ('jsonfield.fields.JSONField', [], {}),
            'current_active_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'microtask': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Microtask']", 'null': 'True'}),
            'original_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'reputation_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'stability': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'static_microtask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.StaticMicrotask']"}),
            'status_flag': ('django.db.models.fields.CharField', [], {'default': "'Raw'", 'max_length': '10'}),
            'submission_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Task']"}),
            'time_to_live': ('django.db.models.fields.FloatField', [], {'default': '100000.0', 'null': 'True'}),
            'translated_sentence': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'translation.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'competence_for_each_language': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_LanguageExpertise']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Master_GeographicalRegion']", 'null': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Master_EducationDomain']", 'null': 'True'}),
            'education_qualification': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['translation.Master_EducationQualification']", 'null': 'True'}),
            'evaluator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['translation.Master_InterestTags']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'translation_userprofile_related_language'", 'default': 'None', 'to': "orm['translation.Master_Language']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'medium_of_education_during_school': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'translation_userprofile_related_medium_of_education'", 'null': 'True', 'blank': 'True', 'to': "orm['translation.Master_Language']"}),
            'no_of_perfect_translations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'overall_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'prev_week_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.Master_Rank']", 'null': 'True'}),
            'total_evaluated_sentences': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_translated_sentences': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_uploaded_tasks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'translator': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'translation.weeklyleaderboard': {
            'Meta': {'object_name': 'WeeklyLeaderboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned_this_week': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['translation.OverallLeaderboard']"}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['translation']
