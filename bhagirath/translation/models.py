from django.db import models
from django.contrib.auth.models import User
import datetime
import jsonfield

class Master_HindiWords(models.Model):
    original = models.CharField(verbose_name="Hindi word",
                                help_text="Hindi word in devnagri script",
                                max_length=2000,
                                null=False,
                                unique=True)
    pos = models.CharField(max_length=2000,null=False)
    
    def __unicode__(self):
        return u"%s" % (self.original)
    
class Master_English2Hindi(models.Model):
    english_word = models.CharField(verbose_name="English word",
                                help_text="English word in dictionary",
                                max_length=2000,
                                null=False,
                                unique=True)
    pos = models.CharField(max_length=2000,null=False)
    hindi_word = models.CharField(verbose_name="Hindi word",
                                help_text="Hindi meaning of english word",
                                max_length=2000,
                                null=False)
    
    def __unicode__(self):
        return u"%s" % (self.english)
    
class Master_AgeGroup(models.Model):
    age_group_tag = models.TextField(verbose_name="Age group",
                                     help_text="Age group",
                                     null = False, 
                                     unique=True)
    minimum_age = models.IntegerField()
    maximum_age = models.IntegerField()
    
    def __unicode__(self):
        return u"%s" % (self.age_group_tag)
    
class Master_GeographicalRegion(models.Model):
    geographical_region = models.TextField(verbose_name="Geographic location",
                                           help_text="Geographic location",
                                           null = False,
                                           unique = True)
    
    def __unicode__(self):
        return u"%s" % (self.geographical_region)

class Master_InterestTags(models.Model):
    category = models.TextField(verbose_name="Task context",
                                help_text="Task context or category",
                                null = False,
                                unique=True)
    need_evaluation = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % (self.category) 
    
class Master_Action(models.Model):
    action = models.TextField(verbose_name="Action name", 
                              help_text="Type of action", 
                              null = False,
                              unique=True)
    
    def __unicode__(self):
        return u"%s" % (self.action)
 
class Master_Role(models.Model):
    role = models.TextField(verbose_name="Role", 
                            help_text="Type of role",
                            null = False,
                            unique=True)
    role_condition = models.TextField(verbose_name="Role activation on", 
                                 help_text="Condition for role activation",
                                 null = True)
    
    def __unicode__(self):
        return u"%s" % (self.role)

class Master_Rank(models.Model):
    position =  models.TextField(verbose_name="Rank", 
                            help_text="Rank of User",
                            null = False,
                            unique=True)
    percentile = models.IntegerField()
    
    def __unicode__(self):
        return u"%s" % (self.position)
 
class Master_EducationQualification(models.Model): 
    education_qualification = models.TextField(verbose_name="Educational qualification", 
                                               help_text="User's educational qualification",
                                               unique=True,
                                               null = False)
    def __unicode__(self):
        return u"%s" % (self.education_qualification)

 
class Master_EducationDomain(models.Model):
    education_qualification = models.ForeignKey(Master_EducationQualification,on_delete=models.PROTECT)
    domain = models.TextField(verbose_name="Domain of education", 
                              help_text="User's educational domain",
                              unique=True,
                              null = False)
    def __unicode__(self):
        return u"%s" % (self.domain) 
    

class Master_Language(models.Model): 
    language = models.TextField(verbose_name="Language", 
                                help_text="Language",
                                unique=True,
                                null = False)
    region = models.TextField(verbose_name="Prevalence region", 
                              help_text="Region where the language is spoken",
                              null = True)
       
    def __unicode__(self):
        return u"%s" % (self.language)

class Master_LanguageExpertise(models.Model): 
    language = models.ForeignKey(Master_Language,on_delete=models.PROTECT)
    expertise = models.IntegerField()
       
    def __unicode__(self):
        return u"%s%s" % (self.language,self.expertise)
    
class StatCounter(models.Model):
    registered_users = models.IntegerField() 
    translated_sentences = models.IntegerField() 
    published_articles = models.IntegerField()
    created_on = models.DateTimeField()
    
    def __unicode__(self):
        return u"%s" % (self.id)
    
class OverallLeaderboard(models.Model):
    username = models.ForeignKey(User,null=False)
    overall_points_earned = models.IntegerField(null=True,default=0)
        
    def __unicode__(self):
        return u"%s" % (self.username)
    
class WeeklyLeaderboard(models.Model):
    username = models.ForeignKey(User,null=False)
    points_earned_this_week = models.IntegerField(null=True,default=0)
    # default = overall_score - prev_week_score from UserProfile
    rank = models.IntegerField(null=True)
        
    def __unicode__(self):
        return u"%s" % (self.username)
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True,on_delete=models.PROTECT)
    date_of_birth = models.DateField(null=False)
    district = models.ForeignKey(Master_GeographicalRegion,on_delete=models.SET_NULL,null=True,default=None)
    education_qualification = models.ForeignKey(Master_EducationQualification,on_delete=models.SET_NULL,null=True,default=None)
    domain = models.ForeignKey(Master_EducationDomain,on_delete=models.SET_NULL,null=True,default=None)
    medium_of_education_during_school = models.ForeignKey(Master_Language,blank=True, null=True,default=None, related_name="%(app_label)s_%(class)s_related_medium_of_education")
    language = models.ManyToManyField(Master_Language,blank=True, null=True,default=None, related_name="%(app_label)s_%(class)s_related_language")
    competence_for_each_language = models.ManyToManyField(Master_LanguageExpertise,blank=True, null=True,default=None)
    translator = models.BooleanField(default=True)
    contributor = models.BooleanField(default=False)
    evaluator = models.BooleanField(default=False)
    interests = models.ManyToManyField(Master_InterestTags,blank=True, null=True,default=None)
    overall_score  = models.IntegerField(default=0)
    prev_week_score = models.IntegerField(default=0)
    total_translated_sentences = models.IntegerField(default=0) 
    total_evaluated_sentences = models.IntegerField(default=0)
    total_uploaded_tasks = models.IntegerField(default=0)
    no_of_perfect_translations = models.IntegerField(default=0)
    rank = models.ForeignKey(Master_Rank,on_delete=models.SET_NULL,null=True) 
    ip_address = models.IPAddressField(null=True)
 
    def __unicode__(self):
        return u"%d" %(self.id)

class Session(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    login_timestamp = models.DateTimeField(null=False)
    logout_timestamp = models.DateTimeField(null=True)

    def __unicode__(self):
        return u"%s" %(self.id)
    
class Task(models.Model):
    html_doc_name = models.URLField(verify_exists=True,null=True,verbose_name="URL referring to file") 
    html_doc_content = models.FileField(upload_to='task_uploads/%Y/%m/%d',null=True)
    upload_timestamp = models.DateTimeField(default=datetime.datetime.now)
    time_to_publish = models.DateTimeField('Time to publish',null=True)
    source_language = models.ForeignKey(Master_Language,related_name="source_language",on_delete=models.PROTECT)
    target_language = models.ForeignKey(Master_Language,related_name="target_language",on_delete=models.PROTECT)
    interest_tags = models.ManyToManyField(Master_InterestTags,null=True)
    context_size = models.IntegerField(verbose_name="Context", 
                                  help_text="Context for microtasks",
                                  null = True)
    budget = models.PositiveIntegerField(default=1,null=True)
    dampening_factor = models.FloatField(default=0.5,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    age_group_tag = models.ForeignKey(Master_AgeGroup,on_delete=models.PROTECT,null=True)
    geographical_region = models.ForeignKey(Master_GeographicalRegion,on_delete=models.PROTECT,null=True)
    published = models.BooleanField(default=False)
        
    class Meta:
        ordering = ['time_to_publish',]
 
    def __unicode__(self):
        return u"%s" % (self.id)

        
class Subtask(models.Model):
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    original_data = models.FileField(upload_to='subtask_original_uploads',null=False)
    translated_data = models.FileField(upload_to='subtask_translated_uploads',null=True)
    current_average_stability = models.FloatField(default=0.0,null=True)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % (self.id)
    
class StaticMicrotask(models.Model):
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT)
    original_sentence = models.CharField(max_length=2000,null=False)
    translated_sentence = models.CharField(max_length=2000,null=True)
    machine_translation = models.CharField(max_length=2000,null=True)
    user = models.ForeignKey(User,null=True)
    assigned = models.BooleanField(default=False)
    stability = models.FloatField(default=0.0,null=True)
    scoring_done = models.BooleanField(default=False)
    hop_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"%s" %(self.id)
    
class Microtask(models.Model):
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT)
    static_microtask = models.ForeignKey(StaticMicrotask,on_delete=models.PROTECT)
    original_sentence = models.CharField(max_length=2000,null=False)
    assign_timestamp = models.DateTimeField(null=False)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" %(self.id)
    
class UserHistory(models.Model):
    STATUS_FLAG_CHOICES = (
        (u'Raw', u'Raw'),
        (u'Reviewed', u'Reviewed'),
        (u'Matured', u'Matured'),
        (u'Pool', u'Pool'),
    )
    
    task = models.ForeignKey(Task,on_delete=models.PROTECT) 
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT)
    static_microtask = models.ForeignKey(StaticMicrotask,on_delete=models.PROTECT)
    microtask = models.ForeignKey(Microtask,null=True,on_delete=models.SET_NULL,default=None)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    original_sentence = models.CharField(max_length=2000,null=False)
    translated_sentence = models.CharField(max_length=2000,null=True)
    assign_timestamp = models.DateTimeField(null=True)
    submission_timestamp = models.DateTimeField(null=True)
    reputation_score = models.IntegerField(default=0,null=True)
    stability = models.FloatField(default=0.0,null=True)
    change_flag = models.BooleanField(default=False)
    time_to_live = models.FloatField(default=100000.0,null=True)
    status_flag = models.CharField(max_length=10,choices=STATUS_FLAG_CHOICES,default="Raw")
    current_active_tag = models.BooleanField(default=False)
    correction_episode = jsonfield.JSONField()
          
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    

class TransactionAction(models.Model):
    session = models.ForeignKey(Session,on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    action = models.ForeignKey(Master_Action,on_delete=models.PROTECT)
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT,null=True)
    static_microtask = models.ForeignKey(StaticMicrotask,on_delete=models.PROTECT,null=True)
    action_timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return u"%s" %(self.id)