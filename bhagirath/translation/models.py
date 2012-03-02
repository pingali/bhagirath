from django.db import models
from django.contrib.auth.models import User
import datetime
import jsonfield

class Master_HindiWords(models.Model):
    """
    This class contains hindi words and it returns hindi word.
    original: hindi word in devanagri
    pos: part of speech - noun, verb, adverb, adjective
    """
    original = models.CharField(verbose_name="Hindi word",
                                help_text="Hindi word in devnagri script",
                                max_length=2000,
                                null=False)
    pos = models.CharField(max_length=2000,null=False)
    
    def __unicode__(self):
        return u"%s" % (self.original)

    class Meta:
        ordering = ["original"]
        
class Master_English2Hindi(models.Model):
    """
    This class contains english word, its hindi meaning, part of speech and returns english word.
    Used for english-hindi dictionary lookup.
    english_word: English word.
    pos: part of speech  
    hindi_word: meaning in hindi (devanagri script)
    """
    english_word = models.CharField(verbose_name="English word",
                                help_text="English word in dictionary",
                                max_length=2000,
                                null=False)
    pos = models.CharField(max_length=2000,null=False)
    hindi_word = models.CharField(verbose_name="Hindi word",
                                help_text="Hindi meaning of english word",
                                max_length=2000,
                                null=False)
    
    def __unicode__(self):
        return u"%s" % (self.english_word)
    
    class Meta:
        ordering = ["english_word"]
        
class Master_AgeGroup(models.Model):
    """
    Contains age group tag along with the minimum and maximum age 
    for that group
    """
    age_group_tag = models.TextField(verbose_name="Age group",
                                     help_text="Age group",
                                     null = False, 
                                     unique=True)
    minimum_age = models.IntegerField()
    maximum_age = models.IntegerField()
    
    def __unicode__(self):
        return u"%s" % (self.age_group_tag)
    
class Master_GeographicalRegion(models.Model):
    """
    Contains districts all over India. 
    These are used to know the geographical region 
    of the user
    """
    geographical_region = models.TextField(verbose_name="Geographic location",
                                           help_text="Geographic location",
                                           null = False,
                                           unique = True)
    
    def __unicode__(self):
        return u"%s" % (self.geographical_region)
    
    class Meta:
        ordering = ["geographical_region"]


class Master_InterestTags(models.Model):
    """
    Contain domain names in order to determine
    the field to which article is related to 
    for ex. history, poetry
    need_evaluation field determines whether this
    article needs evaluation or not 
    """
    category = models.TextField(verbose_name="Task context",
                                help_text="Task context or category",
                                null = False,
                                unique=True)
    need_evaluation = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % (self.category) 
    
    class Meta:
        ordering = ["category"]
    
class Master_Action(models.Model):
    """
     This table has actions that user can perform
    """
    action = models.TextField(verbose_name="Action name", 
                              help_text="Type of action", 
                              null = False,
                              unique=True)
    
    def __unicode__(self):
        return u"%s" % (self.action)

    class Meta:
        ordering = ["action"]
        
class Master_Role(models.Model):
    """
    This table defines all possible roles user can have.
    Depending on the condition on which the role permission
    is granted
    """
    role = models.TextField(verbose_name="Role", 
                            help_text="Type of role",
                            null = False,
                            unique=True)
    role_condition = models.TextField(verbose_name="Role activation on", 
                                 help_text="Condition for role activation",
                                 null = True)
    
    def __unicode__(self):
        return u"%s" % (self.role)

    class Meta:
        ordering = ["role"]

class Master_Rank(models.Model):
    """
    This table defines the rank of the user
    Rank is determined through reputation score algorithm
    """
    position =  models.TextField(verbose_name="Rank", 
                            help_text="Rank of User",
                            null = False,
                            unique=True)
    percentile = models.IntegerField()
    
    def __unicode__(self):
        return u"%s" % (self.position)
 
class Master_EducationQualification(models.Model): 
    """
    This table stores various educational qualifications
    that the users can have
    """
    education_qualification = models.TextField(verbose_name="Educational qualification", 
                                               help_text="User's educational qualification",
                                               unique=True,
                                               null = False)
    def __unicode__(self):
        return u"%s" % (self.education_qualification)

    class Meta:
        ordering = ["education_qualification"]
        
class Master_EducationDomain(models.Model):
    """
    It stores the domain of education of user
    """
    domain = models.TextField(verbose_name="Domain of education", 
                              help_text="User's educational domain",
                              unique=True,
                              null = False)
    def __unicode__(self):
        return u"%s" % (self.domain) 
    
    class Meta:
        ordering = ["domain"]
        
class Master_Language(models.Model): 
    """
    It contains name of the language and the
    region where the language is mostly spoken
    """
    language = models.TextField(verbose_name="Language", 
                                help_text="Language",
                                unique=True,
                                null = False)
    region = models.TextField(verbose_name="Prevalence region", 
                              help_text="Region where the language is spoken",
                              null = True)
       
    def __unicode__(self):
        return u"%s" % (self.language)
    
    class Meta:
        ordering = ["language"]
        
class Master_LanguageExpertise(models.Model): 
    """
    It contains name of the language and the
    score of expertise 
    """
    language = models.ForeignKey(Master_Language,on_delete=models.PROTECT)
    expertise = models.IntegerField()
       
    def __unicode__(self):
        return u"Language:%s  Expertise:%s" % (self.language,self.expertise)
    
    class Meta:
        ordering = ["language"]

class Master_SampleTranslations(models.Model):
    """
    This table stores english sentence, its machine
    translation and user translated sentence 
    """
    original_sentence = models.TextField(verbose_name="Original sentence", 
                                help_text="Sentence in source language",
                                unique=True,
                                null = False)
    google_translation = models.TextField(verbose_name="Google translation", 
                                help_text="Translation from google",
                                unique=True,
                                null = False)
    user_translation = models.TextField(verbose_name="User translation", 
                                help_text="Translation done by user",
                                unique=True,
                                null = False)
    
    def __unicode__(self):
        return u"%s" % (self.id)
    
class Master_Experiment(models.Model):
    """
    This stores a 24 bit array in bit_array field
    The bits are grouped in a way to experiment
    the number of copies that should be made, features
    that should be given or not
    A    B    C    D    E
    3    3    4    1    1
    A - no. of sentences that should be given above for context
    B - no. of sentences that should be given below for context
    C - no. of parallel users
    D - auto correction
    E - Reference translation
    """
    bit_array = models.CharField(max_length=24)
    
    def __unicode__(self):
        return u"%s" % (self.bit_array) 
    

class StatCounter(models.Model):
    """
    it stores the count of registered users,
    sentences and articles translated and 
    the timestamp when it was found
    """
    registered_users = models.IntegerField() 
    translated_sentences = models.IntegerField() 
    published_articles = models.IntegerField()
    created_on = models.DateTimeField()
    
    def __unicode__(self):
        return u"%s" % (self.id)
    
    
class OverallLeaderboard(models.Model):
    """
    Stores all users and total points they scored till date
    """
    username = models.ForeignKey(User,null=False)
    overall_points_earned = models.IntegerField(null=True,default=0)
        
    def __unicode__(self):
        return u"%s" % (self.id)
    
class WeeklyLeaderboard(models.Model):
    """
    Stores top 10 week users depending on their weekly score
    """
    username = models.ForeignKey(User,null=False)
    points_earned_this_week = models.IntegerField(null=True,default=0)
    rank = models.ForeignKey(OverallLeaderboard,null=False)
        
    def __unicode__(self):
        return u"%s" % (self.id)
    
class UserProfile(models.Model):
    """
    advanced user details are stored in this model 
    """
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=6,null=False)
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
    """
    It stores the time for which user was active ie
    user id, time he logged in and logged out
    """
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    login_timestamp = models.DateTimeField(null=False)
    logout_timestamp = models.DateTimeField(null=True)

    def __unicode__(self):
        return u"%s" %(self.id)
    
class Task(models.Model):
    """
    Uploaded file along with its info is stored in this model
    """
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
    parsed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['time_to_publish',]
 
    def __unicode__(self):
        return u"%s" % (self.id)
        
class Subtask(models.Model):
    """
    Extracted text from html doc is stored in this model
    """
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    original_data = models.FileField(upload_to='subtask_original_uploads',null=False)
    translated_data = models.FileField(upload_to='subtask_translated_uploads',null=True)
    current_average_stability = models.FloatField(default=0.0,null=True)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % (self.id)
    
class StaticMicrotask(models.Model):
    """
    sentences that are formed from html text are stored in this table
    """
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
    bit_array = models.ForeignKey(Master_Experiment,null=True)
    
    def __unicode__(self):
        return u"%s" %(self.id)
    
class Microtask(models.Model):
    """
    Stores copies of sentences in StaticMicroatsk table
    initially assigned is false but when it is given to user
    its assigned flag is set to true
    """
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT)
    static_microtask = models.ForeignKey(StaticMicrotask,on_delete=models.PROTECT)
    original_sentence = models.CharField(max_length=2000,null=False)
    assign_timestamp = models.DateTimeField(null=False)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" %(self.id)
    
class UserHistory(models.Model):
    """
    It stores entry for every sentence given to every user
    with various other parameters to determine his performance
    """
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
    """
    Stores actions done by user and time
    It can be uploading file, translating sentence, evaluating sentences 
    """
    session = models.ForeignKey(Session,on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    action = models.ForeignKey(Master_Action,on_delete=models.PROTECT)
    task = models.ForeignKey(Task,on_delete=models.PROTECT)
    subtask = models.ForeignKey(Subtask,on_delete=models.PROTECT,null=True)
    static_microtask = models.ForeignKey(StaticMicrotask,on_delete=models.PROTECT,null=True)
    action_timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return u"%s" %(self.id)