from django.db import models
from django.contrib.auth.models import User
import datetime
    
class Action(models.Model):
    action_name = models.TextField(verbose_name="Action name", 
                                   default="",
                                   help_text="Type of action")
    
    def __unicode__(self):
        return u"%s" % (self.action_name)
 

class Language(models.Model): 
    language_name = models.TextField(verbose_name="Language name", 
                                default="",
                                help_text="Language")
    
    def __unicode__(self):
        return u"%s" % (self.language_name)
    
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    date_of_birth = models.DateField()
    city = models.CharField(verbose_name="City",
                            max_length = 50, 
                            help_text="City to which user belongs")
    language = models.ForeignKey(Language)
    contributor = models.BooleanField(default=False)
    translator = models.BooleanField(default=True)
    interests = models.CharField(verbose_name="Interests", 
                                  max_length = 100, 
                                 help_text="Fields of interests for translation")
    ip_address = models.CharField(max_length = 50)
 
    def __unicode__(self):
        return u"%d" %(self.id)

class Session(models.Model):
    user = models.ForeignKey(User)
    login_timestamp = models.DateTimeField()
    logout_timestamp = models.DateTimeField()

    def __unicode__(self):
        return u"%s" %(self.id)
    
class Task(models.Model):
    html_doc_name = models.FilePathField(max_length=500) 
    html_doc_content = models.FileField(upload_to='task_uploads')
    upload_timestamp = models.DateTimeField(default=datetime.datetime.now)
    time_to_publish = models.DateTimeField('Time to publish',null=True)
    source_language = models.ForeignKey(Language,related_name="source_language")
    target_language = models.ForeignKey(Language,related_name="target_language")
    context = models.IntegerField(verbose_name="Context", 
                                  default=0,
                                  help_text="Context for microtasks",
                                  null = True)
    interest_tags = models.CharField(max_length=5000,null=True)
    budget = models.PositiveIntegerField(default=1,null=True)
    dampening_factor = models.FloatField(default=0.5,null=True)
        
    class Meta:
        ordering = ['time_to_publish',]
 
    def __unicode__(self):
        return u"%s" % (self.html_doc_name)

  
class Subtask(models.Model):
    task = models.ForeignKey(Task)
    original_data = models.FileField(upload_to='subtask_original_uploads')
    translated_data = models.FileField(upload_to='subtask_translated_uploads')
    current_average_stability = models.FloatField(default=0.0)
    

class StaticMicrotask(models.Model):
    task = models.ForeignKey(Task)
    subtask = models.ForeignKey(Subtask)
    original_sentence = models.CharField(max_length=2000)
    translated_sentence = models.CharField(max_length=2000)
    assigned = models.BooleanField(default=False)
    stability = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    

class Microtask(models.Model):
    task = models.ForeignKey(Task)
    subtask = models.ForeignKey(Subtask)
    static_microtask = models.ForeignKey(StaticMicrotask)
    original_sentence = models.CharField(max_length=2000)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    

class TransactionAction(models.Model):
    session = models.ForeignKey(Session)
    user = models.ForeignKey(User)
    action_name = models.ForeignKey(Action)
    task = models.ForeignKey(Task)
    subtask = models.ForeignKey(Subtask)
    microtask = models.ForeignKey(Microtask)
    
    def __unicode__(self):
        return u"%s" %(self.id)
    
    
class UserHistory(models.Model):
    STATUS_FLAG_CHOICES = (
        (u'Raw', u'Raw'),
        (u'Reviewed', u'Reviewed'),
        (u'Matured', u'Matured'),
        (u'Pool', u'Pool'),
    )
    
    task = models.ForeignKey(Task) 
    subtask = models.ForeignKey(Subtask)
    static_microtask = models.ForeignKey(StaticMicrotask)
    microtask = models.ForeignKey(Microtask)
    user = models.ForeignKey(User)
    original_sentence = models.CharField(max_length=2000)
    transliterated_sentence = models.CharField(max_length=2000)
    translated_sentence = models.CharField(max_length=2000,null=True)
    stability = models.FloatField(default=0.0)
    change_flag = models.BooleanField(default=False)
    time_to_live = models.FloatField(default=100000.0)
    status_flag = models.CharField(max_length=10,choices=STATUS_FLAG_CHOICES,default="Raw")
    current_active_tag = models.BooleanField(default=False)
      
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    