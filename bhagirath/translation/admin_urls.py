from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.translation.admin_views',                    
    url(r'^active_users/$', 'active_users', name='active_users'),
    url(r'^complete_user_history/$', 'complete_user_history', name='complete_user_history'),
    url(r'^current_translations/$', 'current_translations', name='current_translations'),
    url(r'^translations_max_hops/$', 'translations_max_hops', name='translations_max_hops'),
    url(r'^translations_min_hops/$', 'translations_min_hops', name='translations_min_hops'),
    url(r'^total_translations/$', 'total_translations', name='total_translations'),
    url(r'^avg_translation_rate/$', 'avg_translation_rate', name='avg_translation_rate'),
    url(r'^avg_convergence_rate/$', 'avg_convergence_rate', name='avg_convergence_rate'),
    url(r'^microtask_similarity_score/$', 'microtask_similarity_score', name='microtask_similarity_score'),
    
    url(r'^populate_subtask/','populate_subtask',name='populate_subtask'),
    url(r'^populate_staticmicrotask/','populate_staticmicrotask',name='populate_staticmicrotask'),
    url(r'^populate_microtask/','populate_microtask',name='populate_microtask'),
    url(r'^unassign_microtask/','unassign_microtask',name='unassign_microtask'),
    url(r'^upload_priviledge/','upload_priviledge',name='upload_priviledge'),
    url(r'^update_weekly_leaderboard/','update_weekly_leaderboard',name='update_weekly_leaderboard'),
    url(r'^update_overall_leaderboard/','update_overall_leaderboard',name='update_overall_leaderboard'),
    url(r'^update_statistics_counter/','update_statistics_counter',name='update_statistics_counter'),
    url(r'^document_stability/','document_stability',name='document_stability'),
    url(r'^reputation_score/','reputation_score',name='reputation_score'),
    url(r'^assign_rank/','assign_rank',name='assign_rank')
)
