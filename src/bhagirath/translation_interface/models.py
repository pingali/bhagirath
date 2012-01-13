from django.db import models
from django.contrib.auth.models import User
import datetime

class Task(models.Model):
    html_doc_name = models.FilePathField(max_length=500) 
    html_doc_content = models.FileField(upload_to='task_uploads')
    upload_timestamp = models.DateTimeField(default=datetime.datetime.now)
    interest_tags = models.CharField(max_length=5000,null=True)
    budget = models.PositiveIntegerField()
    duration = models.DateTimeField('date till needs publishing')
    dampening_factor = models.FloatField(default=0.5)
    current_average_stability = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['upload_timestamp',]
 
    def __unicode__(self):
        return u"%s" % (self.html_doc_name)

  
class Subtask(models.Model):
    task = models.ForeignKey(Task)
    original_data = models.FileField(upload_to='subtask_original_uploads')
    translated_data = models.FileField(upload_to='subtask_translated_uploads')
    time_to_live = models.FloatField(default=1000000.0)
    
    class Meta:
        ordering = ['time_to_live',]
 
 
class UserProfile(models.Model):
    LANGUAGE_CHOICES = (
        (u'Hindi', u'Hindi'),
        (u'Marathi', u'Marathi'),
        (u'Gujrati', u'Gujrati'),
        (u'Tamil', u'Tamil'),
        (u'Telugu', u'Telugu'),
    )
    
    user = models.ForeignKey(User, unique=True) 
    language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES,default="Hindi")
    maximum_load = models.PositiveIntegerField(default=0)
    current_load = models.PositiveIntegerField(default=0)
 
    def __unicode__(self):
        return u"%d" %(self.id)


class StaticMicrotask(models.Model):
    subtask = models.ForeignKey(Subtask)
    task = models.ForeignKey(Task)
    original_sentence = models.CharField(max_length=2000)
    translated_sentence = models.CharField(max_length=2000)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    

class Microtask(models.Model):
    task = models.ForeignKey(Task)
    subtask = models.ForeignKey(Subtask)
    static_microtask = models.ForeignKey(StaticMicrotask)
    original_sentence = models.CharField(max_length=2000)
    translated_sentence = models.CharField(max_length=2000)
    assigned = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    
    
    
class UserHistory(models.Model):
    STATUS_FLAG_CHOICES = (
        (u'Raw', u'Raw'),
        (u'Reviewed', u'Reviewed'),
        (u'Matured', u'Matured'),
        (u'Pool', u'Pool'),
    )
    
    subtask = models.ForeignKey(Subtask)
    task = models.ForeignKey(Task)
    microtask = models.ForeignKey(Microtask)
    original_sentence = models.CharField(max_length=2000)
    transliterated_sentence = models.CharField(max_length=2000)
    translated_sentence = models.CharField(max_length=2000,null=True)
    stability = models.FloatField(default=0.0)
    hop_count = models.PositiveIntegerField()
    change_flag = models.BooleanField(default=False)
    time_to_live = models.FloatField(default=100000.0)
    status_flag = models.CharField(max_length=10,choices=STATUS_FLAG_CHOICES,default="Raw")
    current_active_tag = models.BooleanField(default=False)
    user = models.ForeignKey(User)
      
    def __unicode__(self):
        return u"%s" %(self.original_sentence)
    