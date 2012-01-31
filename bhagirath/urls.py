from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^hindiwords/$','translation.views.hindiwords',name="hindiwords"),
    url(r'^subtask/$','translation.views.subtask',name="subtask"),
    url(r'^staticmicro/$','translation.views.staticmicro',name="staticmicro"),
    url(r'^microtask/$','translation.views.microtask',name="microtask"),
    url(r'^home/$','translation.views.home',name="home"),
    url(r'^aboutUs/$','translation.views.aboutus',name="aboutUs"),
    url(r'^signup/$','translation.views.signup',name="signup"),
    url(r'^signup/done/$','translation.views.processSignup',name="signupDone"),                  
    url(r'^login/$','translation.views.processSignin',name="login"),
    url(r'^logout/$','translation.views.processSignout',name="logout"),
    url(r'^account/$','translation.views.account',name="account"),
    url(r'^account/upload/$','translation.views.upload',name="upload"),
    url(r'^account/upload/done/$','translation.views.uploadDone',name="UploadDone"),
    url(r'^account/evaluate/$','translation.views.evaluate',name="evaluate"),
    url(r'^account/evaluate/done/$','translation.views.evaluateDone',name="EvaluateDone"),
    url(r'^account/translate/(?P<uid>\d+)/$','translation.views.translate',name="translate"),
    url(r'^account/translate/(?P<uid>\d+)/(?P<id>\d+)/done/$','translation.views.translateDone',name="translateDone"),
    url(r'^account/translate/(?P<uid>\d+)/(?P<id>\d+)/context/$','translation.views.context',name="context"),
    url(r'^account/(?P<uid>\d+)/settings/$','translation.views.account_settings',name="account_settings"),
    ('^/?$', redirect_to, {"url": "/home"}),   
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
   

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
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

