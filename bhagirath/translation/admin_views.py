from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Avg, Max, Min

from bhagirath.translation.models import Session as BhagirathSession
from bhagirath.translation.models import *
from django.contrib.auth.models import User
from datetime import timedelta
import datetime

def active_users(request):
    user_id = BhagirathSession.objects.all().filter(logout_timestamp=None).values('user').distinct(true_or_false=True)
    
    dict = {}
    list = []
    for i in user_id:
        k = User.objects.get(pk=i['user'])
        j = BhagirathSession.objects.all().filter(user=k,logout_timestamp=None)
        dict['username'] = k.username
        dict['login_timestamp'] =  j[0].login_timestamp
        list.append(dict)    
    data = {
            'active_users_list':list,
            'count':len(list)
        } 
    return render_to_response('my_admin_tools/menu/active_users.html',data,context_instance=RequestContext(request))         

def current_translations(request):
    list = []
    t = UserHistory.objects.all().exclude(submission_timestamp=None)
    for i in t:
        a = datetime.datetime.now()-i.submission_timestamp
        if a.seconds <= 3600:
            dict = {}  
            dict['username'] = i.user
            dict['original_sentence'] = i.original_sentence
            dict['translated_sentence'] = i.translated_sentence
            list.append(dict)
        
    data = {
            'current_translations':list,
            'count':len(list)
        } 
    return render_to_response('my_admin_tools/menu/current_translations.html',data,context_instance=RequestContext(request))

def translations_max_hops(request):
    list = []
    translations_max_hops = StaticMicrotask.objects.all().filter(scoring_done=True).order_by('hop_count')[:5]
     
    for i in translations_max_hops:
        dict = {}  
        dict['username'] = i.user
        dict['original_sentence'] = i.original_sentence
        dict['translated_sentence'] = i.translated_sentence
        dict['hops'] = i.hop_count
        list.append(dict)
    
    data = {'translations_max_hops':list} 
    return render_to_response('my_admin_tools/menu/translations_max_hops.html',data,context_instance=RequestContext(request))

def translations_min_hops(request):
    list = []
    translations_max_hops = StaticMicrotask.objects.all().filter(scoring_done=True).order_by('-hop_count')[:5]
    
    for i in translations_max_hops:
        dict = {}  
        dict['username'] = i.user
        dict['original_sentence'] = i.original_sentence
        dict['translated_sentence'] = i.translated_sentence
        dict['hops'] = i.hop_count
        list.append(dict)
    
    data = {'translations_max_hops':list} 
    return render_to_response('my_admin_tools/menu/translations_min_hops.html',data,context_instance=RequestContext(request))
     

def total_translations(request):
    total_translations = StaticMicrotask.objects.all().filter(scoring_done=True).count()
    
    data = {'total_translations':total_translations} 
    return render_to_response('my_admin_tools/menu/total_translations.html',data,context_instance=RequestContext(request))

def avg_translation_rate(request):
    t = UserHistory.objects.all().exclude(submission_timestamp=None)
    count = UserHistory.objects.all().count()
    timespan = 0
    max_translation_time = 0 
    min_translation_time = 0
    for i in t:
        s = i.submission_timestamp - i.assign_timestamp
        timespan += s.seconds
        if min_translation_time == 0:
            min_translation_time = s.seconds
        if s.seconds > max_translation_time: 
            max_translation_time = s.seconds
        if s.seconds < min_translation_time: 
            min_translation_time = s.seconds
    
    a = timespan/count
    avg_translation_rate = a/60 
    
    data = {
            'avg_translation_rate':avg_translation_rate,
            'max_translation_time':max_translation_time,
            'min_translation_time':min_translation_time
    } 
    return render_to_response('my_admin_tools/menu/avg_translation_rate.html',data,context_instance=RequestContext(request))

def avg_convergence_rate(request):
    t = StaticMicrotask.objects.all().filter(scoring_done=True).aggregate(Avg('hop_count'),Max('hop_count'),Min('hop_count'))
    
    avg_hop_count = t['hop_count__avg']
    max_hop_count = t['hop_count__max']
    min_hop_count = t['hop_count__min']
    
    data = {
            'avg_hop_count':avg_hop_count,
            'max_hop_count':max_hop_count,
            'min_hop_count':min_hop_count
    } 
    return render_to_response('my_admin_tools/menu/avg_convergence_rate.html',data,context_instance=RequestContext(request))

def microtask_similarity_score(request):
    data = {} 
    return render_to_response('my_admin_tools/menu/microtask_similarity_score.html',data,context_instance=RequestContext(request))
     

     