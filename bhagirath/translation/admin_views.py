from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Avg, Max, Min
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.core import serializers
from bhagirath.translation.models import Session as BhagirathSession
from bhagirath.translation.models import UserHistory as BhagirathUserHistory
from bhagirath.translation.models import RevisedUserHistory as RevisedBhagirathUserHistory
from bhagirath.translation.models import *
#from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import tempMicrotaskParser
from bhagirath.centoid_score.CentroidFinder import CentroidFinder
import traceback, codecs, re
from stemming.porter2 import stem

#############CURRENT ACTIVITY FUNCTIONS###############

def complete_user_history(request):
    """
    This function displays the complete content in the UserHistory table
    """
    #unassign_microtask(request)
    list = []
    complete_user_history = BhagirathUserHistory.objects.all()
    for i in complete_user_history:
        dict = {}  
        dict['username'] = i.user
        dict['original_sentence'] = i.original_sentence
        dict['translated_sentence'] = i.translated_sentence
        dict['assign_timestamp'] = i.assign_timestamp
        dict['submission_timestamp'] = i.submission_timestamp
        list.append(dict)

    overall_user_history = RevisedBhagirathUserHistory.objects.all()
    for i in overall_user_history:
        dict = {}  
        dict['username'] = i.user
        dict['original_sentence'] = i.original_sentence
        dict['translated_sentence'] = i.translated_sentence
        dict['assign_timestamp'] = i.assign_timestamp
        dict['submission_timestamp'] = i.submission_timestamp
        list.append(dict)

    data = {'complete_user_history':list} 
    return render_to_response('my_admin_tools/menu/complete_user_history.html',data,context_instance=RequestContext(request))

def active_users(request):
    """
This function displays currently logged-in users.
"""
    user_id = BhagirathSession.objects.all().filter(logout_timestamp=None).values('user').distinct(true_or_false=True)
    
    dict = {}
    list = []
    for i in user_id:
        k = User.objects.get(pk=i['user'])
        j = BhagirathSession.objects.all().filter(user=k,logout_timestamp=None)
        dict['username'] = k.username
        dict['login_timestamp'] = j[0].login_timestamp
        list.append(dict)
    data = {
            'active_users_list':list,
            'count':len(list)
        }
    return render_to_response('my_admin_tools/menu/active_users.html',data,context_instance=RequestContext(request))

def current_translations(request):
    """
This function displays translations performed in last 1 hour.
"""
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
    """
This function displays translations which required maximum hops to get perfect translation.
"""
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
    """
This function displays translations which required minimum hops to get perfect translation.
"""
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
    """
This function displays total number of perfect translations performed till date.
"""
    total_translations = StaticMicrotask.objects.all().filter(scoring_done=True).count()
    
    data = {'total_translations':total_translations}
    return render_to_response('my_admin_tools/menu/total_translations.html',data,context_instance=RequestContext(request))

def avg_translation_rate(request):
    """
This function displays average translation rate and maximum and minimum time needed for translating sentence.
"""
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
    """
This function displays average convergence rate i.e
average number of hops before convergence is reached for sentences.
"""
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
    """This function shows the current value of similarity for every
microtask with two closest neighbours for different hop counts.
"""
    data = {}
    return render_to_response('my_admin_tools/menu/microtask_similarity_score.html',data,context_instance=RequestContext(request))
     

#############BACKGROUND TASK FUNCTIONS###############
def populate_task(request):
    """
This function takes file from Task table passes it to subtaskparser
for extracting text out of html doc. subtaskparser
parses file removes tags and stores text part in Subtask table
"""
    try:
        #Reading Task table
        latest_task = Task.objects.all().filter(parsed=False).order_by("upload_timestamp")[0]
        filename = latest_task.html_doc_content.path        
        if filename is None:
            data = {'msg':''}
            messages.error(request, "No tasks present for microtasking.")
            return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
        else:
            file = codecs.open(filename, encoding='utf-8')
            text = repr(file.read())
            
            #Subtask entry created
#            sub = Subtask() 
#            sub.task = Task.objects.get(pk = latest_task.id)
#            sub.original_data = text
#            sub.save()
            
            #StaticMicrotask entry created
            code_for_start_original_sentence = "<os>"
            code_for_end_original_sentence = "</os>"
            code_for_start_translated_sentence = "<ts>"
            code_for_end_translated_sentence = "</ts>"

            #Get individual sentences and its translation
            if re.search(code_for_start_original_sentence, text) is not None:
                raw_text = text.split(code_for_start_original_sentence)
                for token in raw_text:
                    if re.search(code_for_end_original_sentence, token) is not None:
                        sentence_pair = token.split(code_for_end_original_sentence)
                        original_sentence = sentence_pair[0]
                        raw_unicode = sentence_pair[1].split(code_for_start_translated_sentence)
                        clean_unicode = raw_unicode[1].split(code_for_end_translated_sentence)
                        machine_translation = clean_unicode[0]

                        staticmicrotask = StaticMicrotask()
                        staticmicrotask.task = latest_task
#                        staticmicrotask.subtask = sub
                        staticmicrotask.bit_array = Master_Experiment.objects.get(pk=4) 
                        staticmicrotask.original_sentence = original_sentence
                        staticmicrotask.assigned = 0
                        staticmicrotask.user = User.objects.get(pk=latest_task.user.id)#
                        staticmicrotask.meaning = dictionary(original_sentence)
                        staticmicrotask.save()
                        staticmicrotask.machine_translation = machine_translation
                        staticmicrotask.meaning = serializers.serialize('json', StaticMicrotask.objects.filter(pk=staticmicrotask.id), fields=('meaning'), ensure_ascii=False)
                        staticmicrotask.save()
                        
            #task record edited
            latest_task.parsed = True
            latest_task.save()
            
        data = {'msg':''}
        messages.success(request, "Task populated successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Populate task failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

def dictionary(sentence):
    words = sentence.split(' ')
    cnt = len(words)
    x = 0
    
    dict = []
    o = [".",",",";","?","!",":","'",")","]","}",'"']
    r = ["'","(","[","{",'"']
    
    while x < cnt:
        s = words[x]
        if s:
            while s[-1] in o or s[0] in r:
                if s[-1] in o:
                    s = s[:-1]
                if s:
                    if s[0] in r:
                        s = s[1:]
                if s:
                    pass    
                else:
                    break
        
        y = s.lower()
        
        mean = Master_English2Hindi.objects.filter(english_word = y)
        if not mean:
            z = stem(y)
            mean = Master_English2Hindi.objects.filter(english_word = z)
        
        for p in mean:
            w =  Master_English2Hindi.objects.get(pk=p.pk)
            mean_dict = {}
            mean_dict['word'] = s
            mean_dict['pos'] = w.pos
            mean_dict['mean'] = w.hindi_word.split("--") 
            dict.append(mean_dict)
        x += 1
    return dict   

      
#def populate_microtask(request):
#    """
#This function makes copies of sentences in StaticMicrotask table
#depending upon the value in bit_array field of StaticMicrotask table
#ranging from 2 to 5. Store these copies in Microtask table.
#"""
#    try:
#        i = 0
#        static = StaticMicrotask.objects.filter(assigned = 0)
#        while i < 10:
#            s = static[i]
#            x = Master_Experiment.objects.get(bit_array = s.bit_array)
#            z = x.bit_array
#            val = int(z[6:10],2)
#            j = 0
#            while j < val:
#                m = Microtask()
#                m.task = s.task
#                m.subtask = s.subtask
#                m.static_microtask = s
#                m.original_sentence = s.original_sentence
#                m.assigned = 0
#                m.assign_timestamp = datetime.datetime.now()
#                m.save()
#                j += 1
#            s.assigned = 1
#            s.save()
#            i += 1
#        data = {'msg':''}
#        messages.success(request, "Microtask populated successfully.")
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
#    except:
#        msg = traceback.format_exc()
#        data = {'msg':msg}
#        messages.error(request, "Populate Microtask failed.")
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
#
#def unassign_microtask(request):
#    """
#This function is used whenever user clicks translate and sentences are given
#to him for translation from microtask table. When sentence is given its
#assigned flag is set to true but if user clicks next without submitting
#translation its translated_sentence field is null. Sentences having such
#fields are unassigned from microtask table so that it can be given to other users.
#"""
#    try:
#        userhist = UserHistory.objects.all()
#        i = UserHistory.objects.all().count()
#        j = 0
#        count = 0
#        while j < i:
#            u = userhist[j]
#            if u.translated_sentence:
#                pass
#            else:
#                m = u.microtask
#                if m.assigned == True:
#                    m.assigned = 0
#                    m.save()
#                    count += 1
#            j += 1
#        UserHistory.objects.filter(translated_sentence=None).delete()
#        msg = str(count) + " microtasks are unassigned successfully."
#        data = {'msg':msg}
#        messages.success(request, msg)
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
#    except:
#        msg = traceback.format_exc()
#        data = {'msg':msg}
#        messages.error(request, "Unassign Microtask failed.")
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

def upload_priviledge(request):
    """
This function grants user upload file privilege if he checks the
upload checkbox in sign up form
"""
    try:
        check = UserProfile.objects.filter(contributor = 1)
        uncheck = UserProfile.objects.filter(contributor = 0)
    
        i = UserProfile.objects.filter(contributor=1).count()
        k = UserProfile.objects.filter(contributor = 0).count()
            
        j = 0
        while j < i:
            c = check[j]
            usr = User.objects.get(username=c.user)
            perm_id = Permission.objects.get(codename = 'add_task')
            if usr.has_perm('translation.add_task'):
                pass
            else:
                usr.user_permissions.add(perm_id)
                usr.save()
            j += 1
        j = 0
        while j < k:
            u = uncheck[j]
            usr = User.objects.get(username=u.user)
            if not usr.has_perm('translation.add_task'):
                pass
            else:
                usr.user_permissions.remove(perm_id)
                usr.save()
            j += 1
    
        data = {'msg':''}
        messages.success(request, "User's upload priviledge updated successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Update user's upload priviledge failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

def update_overall_leaderboard(request):
    """
This function stores the users in descending order of their overall scores.
While displaying overall leaderboard top 10 users are
selected from the table.
"""
    try:
        user = UserProfile.objects.order_by('-overall_score')
        count = UserProfile.objects.all().count()
        entries = OverallLeaderboard.objects.all().count()
        
        if entries > 0:
            over = OverallLeaderboard.objects.all().delete()
        i = 0
        while i < count:
            over = OverallLeaderboard()
            over.username = user[i].user
            over.overall_points_earned = user[i].overall_score
            over.save()
            i += 1
            
        data = {'msg':''}
        messages.success(request, "Overall Leaderboard updated successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Update Overall Leaderboard failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

def update_weekly_leaderboard(request):
    """
This function stores the 10 users in descending order of their weekly
scores. While displaying weekly leaderboard users are
selected from this table. It remains static for a week
"""
    
    """NOTE:Always execute this after executing Overall leader board"""
    
    try:
        user = UserProfile.objects.order_by('-prev_week_score')
        count = UserProfile.objects.order_by('-prev_week_score').count()
        if count > 10:
            count = 10
        entries = WeeklyLeaderboard.objects.all().count()
        if entries > 0:
            week = WeeklyLeaderboard.objects.all()
            i = 0
            while i < count:
                w = week[i]
                w.username = user[i].user
                w.rank = OverallLeaderboard.objects.get(username = user[i].user)
                w.points_earned_this_week = user[i].prev_week_score
                w.save()
                i += 1
        else:
            i = 0
            while i < count:
                w = WeeklyLeaderboard()
                w.username = user[i].user
                w.rank = OverallLeaderboard.objects.get(username = user[i].user)
                w.points_earned_this_week = user[i].prev_week_score
                w.save()
                i += 1
        userpro = UserProfile.objects.all()
        count = UserProfile.objects.all().count()
        i = 0
        while i < count:
            u = userpro[i]
            u.prev_week_score = 0
            u.save()
            i += 1
        
        data = {'msg':''}
        messages.success(request, "Weekly Leaderboard updated successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Update Weekly Leaderboard failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

def update_statistics_counter(request):
    """
This function updates the statistics- no. of users, no. of sentences
and articles translated periodically and stores in a table
along with the timestamp.
"""
    try:
        u = UserProfile.objects.all().count()
        s = StaticMicrotask.objects.filter(scoring_done=1).count()
        a = Task.objects.filter(published=1).count()
            
        st = StatCounter()
        st.registered_users = u
        st.translated_sentences = s
        st.published_articles = a
        st.created_on = datetime.datetime.now()
        st.save()
        
        data = {'msg':''}
        messages.success(request, "Website statistics updated successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Update Website statistics failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
  
def document_stability(request):
    pass
    #msg = traceback.format_exc()
    #data = {'msg':msg}
    #messages.success(request, "Document stability calculation successfully.")
    data= {'msg':''}
    return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))

#def reputation_score(request):
#    """
#This function finds scores by using centroid_score algorithm for
#the sentences translated by the users. Users are given
#scores for their translation and best translated
#sentence is determined for a particular english sentence.
#If translations are not satisfactory they are given to other
#users for translation.
#"""
#    unassign_microtask(request)
#    try:
#        static = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0)
#        i = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0).count()
#        k = 0
#        while k < i:
#            a = static[k]
#            if a:
#                user = UserHistory.objects.filter(static_microtask = a.id)
#                l = UserHistory.objects.filter(static_microtask = a.id).count()
#                user_responses = []
#                j = 0
#                while j < l:
#                    u = user[j]
#                    if u.translated_sentence:
#                        user_responses.append(u)
#                    else:
#                        pass
#                    j += 1
#                
#                count = len(user_responses)
#                n = count
#                if (n % 3)==0 and n!=0:
#                    p = 0
#                    input1 = []
#                    while p<count:
#                        input1.append(user[p].translated_sentence)
#                        p += 1
#                    v = StaticMicrotask.objects.get(pk=a.id)
#                    input1.append(v.machine_translation)
#                    
#                    centroid = CentroidFinder.getCentroid(input1)
#                    
#                    st = StaticMicrotask.objects.get(id = str(user[0].static_microtask))
#                    st.translated_sentence = centroid
#                    
#                    scores = [int() for __idx0 in range(count)]
#                    scores = CentroidFinder.getReputationscores()
#                    
#                    isAnotherRunNeeded = CentroidFinder.isIterationNeeded()
#                    
#                    if not isAnotherRunNeeded:
#                        z = 0
#                        while z < count:
#                            a = user[z]
#                            a.reputation_score = scores[z]
#                            a.save()
#                            u = UserProfile.objects.get(user = user[z].user)
#                            u.prev_week_score += scores[z]
#                            u.overall_score += scores[z]
#                            if user[z].translated_sentence == centroid:
#                                u.no_of_perfect_translations += 1
#                                st.user = user[z].user
#                            u.save()
#                            user[z].save()
#                            z += 1
#                            
#                        st.scoring_done = 1
#                        st.save()
#                        
#                        """perform clean-up task : Delete related entries from Microtask table and
#move related entries from UserHistory to RevisedUserHistory."""
#                        a = UserHistory.objects.filter(static_microtask = st.id)
#                        for m in a:
#                            r = RevisedUserHistory()
#                            r.task = m.task
#                            r.subtask = m.subtask
#                            r.static_microtask = m.static_microtask
#                            r.user = m.user
#                            r.original_sentence = m.original_sentence
#                            r.translated_sentence = m.translated_sentence
#                            r.assign_timestamp = m.assign_timestamp
#                            r.submission_timestamp = m.submission_timestamp
#                            r.reputation_score = m.reputation_score
#                            r.correction_episode = m.correction_episode
#                            r.save()
#                             
#                        UserHistory.objects.filter(static_microtask = st.id).delete()
#                        Microtask.objects.filter(static_microtask = st.id).delete()
#                    else:
#                        st.assigned = 0
#                        st.hop_count += 1
#                        st.save()
#                k += 1
#        data = {'msg':''}
#        messages.success(request, "User's reputation score updated successfully.")
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
#    except:
#        msg = traceback.format_exc()
#        data = {'msg':msg}
#        messages.error(request, "Update user's reputation score failed.")
#        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
       
def assign_rank(request):
    """
This function is used to assign ranks to users depending upon their position among all the users.
Ranks are categorized as - Amateur, Active translator, Senior translator, Master translator and Rockstar.
"""
    try:
        user = UserProfile.objects.order_by('overall_score')
        count = UserProfile.objects.all().count()
        rockstar = 0.01 * count
        if int(rockstar) < rockstar:
            rockstar = int(rockstar) + 1
    
        master = 0.04 * count
        if int(master) < master:
            master = int(master) + 1
    
        senior = 0.15 * count
        if int(senior) < senior:
            senior = int(senior) + 1
    
        active = 0.3 * count
        if int(active) < active:
            active = int(active) + 1
    
        amateur = 0.5 *count
        if int(amateur) < amateur:
            amateur = int(amateur) + 1
                
        j = 0
        while j < amateur and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Amatuer")
            u.save()
            j += 1
    
        k = 0
        while k < active and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Active translator")
            u.save()
            j += 1
            k += 1
    
        k = 0
        while k < senior and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Senior translator")
            u.save()
            j += 1
            k += 1
    
        k = 0
        while k < master and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Master translator")
            u.save()
            j += 1
            k += 1
    
        while j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Rockstar translator")
            u.save()
            j += 1
    
        
        data = {'msg':''}
        messages.success(request, "Rank assigned to user successfully.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request))
    except:
        msg = traceback.format_exc()
        data = {'msg':msg}
        messages.error(request, "Update user's reputation score failed.")
        return render_to_response('my_admin_tools/menu/background_task.html',data,context_instance=RequestContext(request)) 