from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User, Permission
from bhagirath.translation.models import *
from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import tempMicrotaskParser
from bhagirath.centoid_score.CentroidFinder import CentroidFinder 
import datetime

#1.Populate Subtask - DONE
class PopulateSubtaskCronJob(CronJobBase):
    """
    This class takes file from Task table passes it to subtaskparser
    for extracting text out of html doc. subtaskparser
    parses file removes tags and stores text part in Subtask table
    """
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_subtask_cron_job' # a unique code

    def job(self):
        tasks = Task.objects.all().filter(parsed=False)
        i = Task.objects.all().filter(parsed=False).count()
        j = 0
        while  j < i:
            t = tasks[j]
            a = t.html_doc_content
            subtaskParser(a.path,t.id)
            t.parsed = True
            t.save()
            j +=1

#2.Populate StaticMicortask - DONE
class PopulateStaticMicrotaskCronJob(CronJobBase):
    """
    This class calls microtask parser that takes text part from subtask table,
    splits it into sentences and stores in StaticMicrotask table   
    """
    RUN_EVERY_MINS = 60 # run every 1 hr
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_staticmicrotask_cron_job' # a unique code

    def job(self):
        i = 0
        while i < 5:
            tempMicrotaskParser()
            i += 1

#3.Populate Microtask - DONE
class PopulateMicrotaskCronJob(CronJobBase):
    """
    This class makes copies of sentences in StaticMicrotask table
    depending upon the value in bit_array field of StaticMicrotask table
    ranging from 2 to 5. Store these copies in Microtask table. 
    """
    RUN_EVERY_MINS = 10 # run every 10 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_microtask_cron_job' # a unique code

    def job(self):
        i = 0
        static = StaticMicrotask.objects.filter(assigned = 0)
        while i < 10:
            s = static[i]
            x = Master_Experiment.objects.get(bit_array = s.bit_array)
            z = x.bit_array
            val = int(z[6:10],2) 
            j = 0
            while j < val:
                m = Microtask()
                m.task = s.task
                m.subtask = s.subtask
                m.static_microtask = s
                m.original_sentence = s.original_sentence
                m.assigned = 0
                m.assign_timestamp = datetime.datetime.now()
                m.save()
                j += 1
            s.assigned = 1
            s.save()
            i += 1

#4.Unassign Microtask - DONE
class UnassignMicrotaskCronJob(CronJobBase):
    """
    This class is used whenever user clicks translate and sentences are given 
    to him for translation from microtask table. When sentence is given
    its assigned flag is set to true but if user clicks next without
    submitting translation its translated_sentence field is null
    Sentences having such fields are unassigned from microtask table
    so that it can be given to other users 
    """
    RUN_EVERY_MINS = 10 # run every 10 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.unassign_microtask_cron_job' # a unique code

    def job(self):
        userhist = UserHistory.objects.all()
        i = UserHistory.objects.all().count()
        j = 0
        while j < i:
            u = userhist[j]
            if u.translated_sentence:
                pass
            else:
                m = u.microtask
                m.assigned = 0
                m.save()
            j += 1 
        UserHistory.objects.filter(translated_sentence=None).delete()
        
#5.Assign Upload priviledge - DONE
class UploadPriviledgeCronJob(CronJobBase):
    """
    This class grants user upload file privilege if he checks the
    upload checkbox in sign up form
    """
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_priviledge_cron_job' # a unique code

    def job(self):
        check = UserProfile.objects.filter(contributor = 1)
        uncheck = UserProfile.objects.filter(contributor = 0)

        i =  UserProfile.objects.filter(contributor=1).count()
        k =  UserProfile.objects.filter(contributor = 0).count()     
        
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
        
#6.Update Overall LeaderBoard - DONE
class UpdateOverallLeaderBoardCronJob(CronJobBase):
    """
    This class stores the users in descending order of their overall scores.
    While displaying overall leaderboard top 10 users are
    selected from the table.
    """
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_overall_leaderboard_cron_job' # a unique code

    def job(self):
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
            
#7.Update Weekly LeaderBoard - DONE    
class UpdateWeeklyLeaderBoardCronJob(CronJobBase):
    """
    This class stores the 10 users in descending order of their weekly 
    scores. While displaying weekly leaderboard users are
    selected from this table. It remains static for a week 
    """
    
    """NOTE:Always execute this after executing Overall leader board"""
    RUN_EVERY_MINS = 1440*7 # run every week
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_weekly_leaderboard_cron_job' # a unique code

    def job(self):
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

#8.Update Statistics Counter - DONE    
class UpdateStatisticsCounterCronJob(CronJobBase):
    """
    This class updates the statistics- no. of users, no. of sentences 
    and articles translated periodically and stores in a table 
    along with the timestamp 
    """
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_statistics_counter_cron_job' # a unique code
    
    def job(self):
        u = UserProfile.objects.all().count()
        s = StaticMicrotask.objects.filter(scoring_done=1).count()
        a = Task.objects.filter(published=1).count()
        
        st = StatCounter()        
        st.registered_users = u
        st.translated_sentences = s
        st.published_articles = a
        st.created_on = datetime.datetime.now() 
        st.save()
             
#9.Document stability - This will calculate the overall stability of a document. - PENDING
class DocumentStabilityCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.document_stability_cron_job' # a unique code
    
    def job(self):
        pass

#10.Update Reputation Score - DONE
class ReputationScoreCronJob(CronJobBase):
    """
    This class finds scores by using centroid_score algorithm for
    the sentences translated by the users. Users are given 
    scores for their translation and best translated 
    sentence is determined for a particular english sentence.
    If translations are not satisfactory they are given to other
    users for translation. 
    """
    RUN_EVERY_MINS = 60 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.reputation_score_cron_job' # a unique code
    
    def job(self):
        #unassign all microtasks first
        userhist = UserHistory.objects.all()
        i = UserHistory.objects.all().count()
        j = 0
        while j < i:
            u = userhist[j]
            if u.translated_sentence:
                pass
            else:
                m = u.microtask
                m.assigned = 0
                m.save()
            j += 1
        UserHistory.objects.filter(translated_sentence=None).delete()
        
        #code for reputation score starts here
        static = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0)
        i = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0).count()
        k = 0
        while k < i:
            a = static[k]
            if a:
                user = UserHistory.objects.filter(static_microtask = a.id)
                l = UserHistory.objects.filter(static_microtask = a.id).count()
                user_responses = []
                j = 0
                while j < l:
                    u = user[j]
                    if u.translated_sentence:
                        user_responses.append(u)
                    else:
                        pass
                    j += 1
                
                count = len(user_responses)
                n = count
                if (n % 3)==0 and n!=0:
                    p = 0
                    input1 = []
                    while p<count:
                        input1.append(user[p].translated_sentence)
                        p += 1
                    v = StaticMicrotask.objects.get(pk=a.id)
                    input1.append(v.machine_translation)
                    
                    centroid = CentroidFinder.getCentroid(input1)
                    
                    st = StaticMicrotask.objects.get(id = str(user[0].static_microtask))
                    st.translated_sentence = centroid
                    
                    scores = [int() for __idx0 in range(count)]
                    scores = CentroidFinder.getReputationscores()
                    
                    isAnotherRunNeeded = CentroidFinder.isIterationNeeded()
                    
                    if not isAnotherRunNeeded:
                        z = 0
                        while z < count:
                            a = user[z]
                            a.reputation_score = scores[z]
                            a.save()
                            u = UserProfile.objects.get(user = user[z].user)
                            u.prev_week_score += scores[z]
                            u.overall_score += scores[z]
                            if user[z].translated_sentence == centroid:
                                u.no_of_perfect_translations += 1
                                st.user = user[z].user
                            u.save()
                            user[z].save()
                            z += 1
                            
                        st.scoring_done = 1
                        st.save()
                        
                        """perform clean-up task : Delete related entries from Microtask table 
                        and move related entries from UserHistory to RevisedUserHistory."""
                        a = UserHistory.objects.filter(static_microtask = st.id)
                        for m in a:
                            r = RevisedUserHistory()
                            r.task = m.task
                            r.subtask = m.subtask
                            r.static_microtask = m.static_microtask
                            r.user = m.user
                            r.original_sentence = m.original_sentence
                            r.translated_sentence = m.translated_sentence
                            r.assign_timestamp = m.assign_timestamp
                            r.submission_timestamp = m.submission_timestamp
                            r.reputation_score = m.reputation_score
                            r.correction_episode = m.correction_episode
                            r.save()
                             
                        UserHistory.objects.filter(static_microtask = st.id).delete()
                        Microtask.objects.filter(static_microtask = st.id).delete()
                    else:
                        st.assigned = 0
                        st.hop_count += 1
                        st.save()
                k += 1

#11.Assign Rank-Start from end take upper roundoff of percentage value n assign that rank to those users - DONE
class AssignRankCronJob(CronJobBase):
    """
    This class is used to assign ranks to users depending upon their position among all the users.
    Ranks are categorized as - Amateur, Active translator, Senior translator, Master translator and Rockstar. 
    """
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.assign_rank_cron_job' # a unique code
    
    def job(self):    
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
        while j < amateur  and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Amatuer")   
            u.save()
            j += 1

        k = 0
        while k < active  and j < count:
            u = user[j]
            u.rank = Master_Rank.objects.get(position="Active translator") 
            u.save()
            j += 1
            k += 1

        k = 0
        while k < senior  and j < count:
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