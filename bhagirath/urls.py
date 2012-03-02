from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from bhagirath.translation import admin_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('translation.views', 
    
    #loading home page of bhagirath
    url(r'^home/$','home',name="home"),
    #Displaying about_us template that gives more info about bhagirath
    url(r'^about_us/$','about_us',name="about_us"),
    #Displaying sample_translations template that provides few translations
    url(r'^sample_translations/(?P<id>\d+)/$','sample_translations',name="sample_translations"),
    #Sign up form for registration of new users
    url(r'^sign_up/$','sign_up',name="sign_up"),
    #Get user entered info and store in database when user presses submit button on sign up
    url(r'^sign_up/done/$','process_sign_up',name="process_sign_up"),
    #checks if username and password are authenticated and allow further login
    url(r'^login/$','process_sign_in',name="login"),
    #logs out user and redirects him to home page
    url(r'^logout/$','process_sign_out',name="logout"),
    #loads user account template showing his contribution in bhagirath
    url(r'^account/$','account',name="account"),
    #provides user upload file facility and asks him to enter specified info about file
    url(r'^account/upload/$','upload',name="upload"),
    #stores file and info entered by user when user presses submit button on upload page
    url(r'^account/upload/done/$','process_upload',name="process_upload"),
    #provide users sentences to evaluate
    url(r'^account/evaluate/$','evaluate',name="evaluate"),
    #stores the sentence evaluated by user
    url(r'^account/evaluate/done/$','process_evaluate',name="process_evaluate"),
    #give sentence to user for translation
    url(r'^account/translate/(?P<uid>\d+)/$','translate',name="translate"),
    #stores user entered translation when user hits submit on translate form
    url(r'^account/translate/(?P<uid>\d+)/(?P<id>\d+)/done/$','process_translate',name="process_translate"),
    #displays user entered info which user can edit except username 
    url(r'^account/(?P<uid>\d+)/settings/$','account_settings',name="account_settings"),
    #saves the changes made by user in his profile
    url(r'^account/(?P<uid>\d+)/settings/done/$','process_account_settings',name="process_account_settings"),
   
)

urlpatterns += patterns('',
    ('^/?$', redirect_to, {"url": "/home"}),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
        
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        
    #adding django-admin-tools urls.
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^current_activity/', include(admin_urls)),
    url(r'^background_task/', include(admin_urls)),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )