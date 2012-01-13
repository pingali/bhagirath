from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
     url(r'^login/$','translation_interface.views.home',name="home"),
    url(r'^signup/$','translation_interface.views.processSignup',name="signup"),                  
    url(r'^signin/$','translation_interface.views.processSignin',name="signin"),
    url(r'^signout/$','translation_interface.views.processSignout',name="signout"),
    url(r'^home/upload/$','translation_interface.views.upload',name="upload"),
    url(r'^home/upload/process/$','translation_interface.views.processUpload',name="processUpload"),
    url(r'^home/translate/(?P<uid>\d+)/$','translation_interface.views.translate',name="translate"),
    url(r'^home/translate/(?P<id>\d+)/(?P<uid>\d+)/done/$','translation_interface.views.translationDone',name="translationDone"),
    
    # Examples:
    # url(r'^$', 'bhagirath.views.home', name='home'),
    # url(r'^bhagirath/', include('bhagirath.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )