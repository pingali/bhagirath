from django_cron import CronJobBase, Schedule
from bhagirath.translation.models import Task, UserHistory, StaticMicrotask, Microtask,UserProfile,StatCounter
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
        i = 0
        for j in tasks:
            i += 1
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
        while i < 2:
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
            i += 1

#4.Unassign Microtask - DONE
class UnassignMicrotaskCronJob(CronJobBase):
    RUN_EVERY_MINS = 10 # run every 10 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.unassign_microtask_cron_job' # a unique code

    def job(self):
        i = 0
        userhist = UserHistory.objects.all()
        for k in userhist:
            i += 1
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

#5.Assign Upload priviledge - PENDING
class UploadPriviledgeCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_priviledge_cron_job' # a unique code

    def job(self):
        pass
#6.Update LeaderBoard - PENDING
class UpdateOverallLeaderBoardCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_overall_leaderboard_cron_job' # a unique code

    def job(self):
        pass
    
class UpdateWeeklyLeaderBoardCronJob(CronJobBase):
    """Always execute this after executing Overall leader board"""
    RUN_EVERY_MINS = 1440*7 # run every week
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_weekly_leaderboard_cron_job' # a unique code

    def job(self):
         """overall_score(200) - prev_week_score(180)  = current_week_score
            eg: 200 - 180 = 20 (current_week_score)
            after this prev_week_score = overall_score Background task
        """

#7.Update Statistics Counter - DONE    
class UpdateStatisticsCounterCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.update_statistics_counter_cron_job' # a unique code
    
    def job(self):
        s = 0
        a = 0
        u = UserProfile.objects.all().count()
        smt = StaticMicrotask.objects.filter(scoring_done=1)
        for j in smt:
            s += 1
        art = Task.objects.filter(published=1)
        for j in art:
            a += 1
        
        sta = StatCounter.objects.all()
        st = sta[0]    
        st.registered_users = u
        st.translated_sentences = s
        st.published_articles = a
        st.save()
             
#8.Document stability - This will calculate the overall stability of a document. - PENDING
class DocumentStabilityCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.document_stability_cron_job' # a unique code
    
    def job(self):
        pass

#9.Update Reputation Score - PENDING
class ReputationScoreCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.reputation_score_cron_job' # a unique code
    
    def job(self):
        static = StaticMicrotask.objects.filter(assigned = 1, scoring_done = 0)
        i = 0
        for j in static:
            i += 1
        k = 0
        while k < i:
            user = UserHistory.objects.filter(static_microtask  = static[k].id)
            l = 0
            for j in user:
                l += 1
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
                input = []
                while p<count:
                    input.append(user[p].transliterated_sentence)
                    p += 1
                centroid = CentroidFinder.getCentroid(input)
                #print "centroid" 
                #print centroid
                isAnotherRunNeeded = CentroidFinder.isIterationNeeded()
                if isAnotherRunNeeded:
                    #print "No need for another Iteration"
                    s = StaticMicrotask.objects.filter(id = user[0].static_microtask)
                    st = s[0]
                    st.transliterated_sentence = centroid
                    tr = UserHistory.objects.filter(transliterated_sentence = centroid)
                    t = tr[0]
                    st.translated_sentence =  t.translated_sentence            
                    scores = [int() for __idx0 in range(count)]
                    scores = CentroidFinder.getReputationscores()
                    z = 0
                    while z < count:
                        print scores[i]
                        user[z].reputation_score = scores[z]
                        user[z].save
                        z += 1
                    st.scoring_done = 1
                    st.save()
                else:
                    s = StaticMicrotask.objects.filter(id = user[0].static_microtask)
                    st = s[0]
                    st.assigned = 0
                    st.save()
                    #print "There is a need for another Iteration"


#10.Assign Rank-Start from end take upper roundoff of percentage value n assign that rank to those users - PENDING
class AssignRankCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # run every day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bhagirath.translation.assign_rank_cron_job' # a unique code
    
    def job(self):    
        pass           