from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.translation.admin_views',                    
    url(r'^active_users/$', 'active_users', name='active_users'),
    url(r'^current_translations/$', 'current_translations', name='current_translations'),
    url(r'^translations_max_hops/$', 'translations_max_hops', name='translations_max_hops'),
    url(r'^translations_min_hops/$', 'translations_min_hops', name='translations_min_hops'),
    url(r'^total_translations/$', 'total_translations', name='total_translations'),
    url(r'^avg_translation_rate/$', 'avg_translation_rate', name='avg_translation_rate'),
    url(r'^avg_convergence_rate/$', 'avg_convergence_rate', name='avg_convergence_rate'),
    url(r'^microtask_similarity_score/$', 'microtask_similarity_score', name='microtask_similarity_score'),
)
