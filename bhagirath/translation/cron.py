from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User, Permission
from bhagirath.translation.models import *
from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import microtaskParser
from bhagirath.centoid_score.CentroidFinder import CentroidFinder 
import datetime

#1.Populate Subtask - DONE
class PopulateSubtaskCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_subtask_cron_job' # a unique code
    
    def job(self):
        tasks = Task.objects.all()
        i = Task.objects.all().count()
        j = 0
        while  j< i:
            t = tasks[j]
            subtaskParser(t.html_doc_name)
            j +=1

#2.Populate StaticMicortask - DONE
class PopulateStaticMicrotaskCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # run every 1 hr
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_staticmicrotask_cron_job' # a unique code
    
    def job(self):
        i = 0
        while i < 5:
            microtaskParser()
            i += 1

#3.Populate Microtask - DONE
class PopulateMicrotaskCronJob(CronJobBase):
    RUN_EVERY_MINS = 10 # run every 10 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.populate_microtask_cron_job' # a unique code

    def job(self):
        i = 0
        static = StaticMicrotask.objects.filter(assigned = 0)
        while i < 50:
            s = static[i]
            j = 0
            while j < 3:
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
                micro = Microtask.objects.filter(assigned = 1 , original_sentence = u.original_sentence)
                m = micro[0]
                m.assigned = 0
                m.save()
            j += 1 

#5.Assign Upload priviledge - DONE
class UploadPriviledgeCronJob(CronJobBase):
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
            if  not usr.has_perm('translation.add_task'):
                pass
            else:
                usr.user_permissions.remove(perm_id)        
                usr.save()
            j += 1
        
#6.Update Overall LeaderBoard - DONE
class UpdateOverallLeaderBoardCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_overall_leaderboard_cron_job' # a unique code

    def job(self):
        user = UserProfile.objects.order_by('-overall_score')
        count = UserProfile.objects.all().count()
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
    """Always execute this after executing Overall leader board"""
    RUN_EVERY_MINS = 1440*7 # run every week
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_weekly_leaderboard_cron_job' # a unique code

    def job(self):
        user = UserProfile.objects.order_by('-prev_week_score')
        week = OverallLeaderboard.objects.all()
        i = 0   
        while i < 10:
            w = week[i]
            w.username = user[i].user
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
    RUN_EVERY_MINS = 60 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.reputation_score_cron_job' # a unique code
    
    def job(self):
        static = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0)
        i = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0).count()
        k = 0
        while k < i:
            user = UserHistory.objects.filter(static_microtask = static[k].id)
            l = UserHistory.objects.filter(static_microtask = static[k].id).count()
            j = 0
            while j < l:
                u = user[j]
                if u.translation:
                    pass
                else:
                    u.delete()
                j += 1
            count = 0
            for a in user:
                count += 1
            n = 1
            while n <= 10:
                m = 3 * n
                if count == m:
                    break
                else:
                    pass
                n += 1
            if n == 11: 
                break
            else:
                #count += 1
                p = 0
                input1 = []
                while p<count:
                    input1.append(user[p].translated_sentence)
                    p += 1
                centroid = CentroidFinder.getCentroid(input1)
                    #print "centroid" 
                    #print centroid
                isAnotherRunNeeded = CentroidFinder.isIterationNeeded()
                if not isAnotherRunNeeded:
                        #print "No need for another Iteration"
                    st = StaticMicrotask.objects.get(id = user[0].static_microtask)
                    st.translated_sentence = centroid
                    scores = [int() for __idx0 in range(count)]
                    scores = CentroidFinder.getReputationscores()
                    z = 0
                    while z < count:
                        user[z].reputation_score = scores[z]
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
                else:
                    st = StaticMicrotask.objects.get(id = user[0].static_microtask)
                    st.assigned = 0
                    st.hop_count += 1
                    st.save()

#11.Assign Rank-Start from end take upper roundoff of percentage value n assign that rank to those users - DONE
class AssignRankCronJob(CronJobBase):
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
        while j < amateur:
            u = user[j]
            u.rank = "Amateur"    
            u.save()
            j += 1

        k = 0
        while k < active:
            u = user[j]
            u.rank = "Active translator" 
            u.save()
            j += 1
            k += 1

        k = 0
        while k < senior:
            u = user[j]
            u.rank = "Senior translator"  
            u.save()
            j += 1
            k += 1

        k = 0
        while k < master and j < count:
            u = user[j]
            u.rank = "Master translator" 
            u.save()
            j += 1
            k += 1

        while j < count:
            u = user[j]
            u.rank = "Rockstar translator" 
            u.save()
            j += 1         