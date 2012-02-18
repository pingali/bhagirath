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
    url(r'^english2hindi/$','translation.views.english2hindi',name="english2hindi"),
    url(r'^about_us/$','translation.views.about_us',name="about_us"),
    url(r'^sample_translations/(?P<id>\d+)/$','translation.views.sample_translations',name="sample_translations"),
    url(r'^sign_up/$','translation.views.sign_up',name="sign_up"),
    url(r'^sign_up/done/$','translation.views.process_sign_up',name="process_sign_up"),                  
    url(r'^login/$','translation.views.process_sign_in',name="login"),
    url(r'^logout/$','translation.views.process_sign_out',name="logout"),
    url(r'^account/$','translation.views.account',name="account"),
    url(r'^account/upload/$','translation.views.upload',name="upload"),
    url(r'^account/upload/done/$','translation.views.process_upload',name="process_upload"),
    url(r'^account/evaluate/$','translation.views.evaluate',name="evaluate"),
    url(r'^account/evaluate/done/$','translation.views.process_evaluate',name="process_evaluate"),
    url(r'^account/translate/(?P<uid>\d+)/$','translation.views.translate',name="translate"),
    url(r'^account/translate/(?P<uid>\d+)/(?P<id>\d+)/done/$','translation.views.process_translate',name="process_translate"),
    url(r'^account/translate/(?P<uid>\d+)/(?P<id>\d+)/context/$','translation.views.load_context',name="load_context"),
    url(r'^account/(?P<uid>\d+)/settings/$','translation.views.account_settings',name="account_settings"),
    url(r'^account/(?P<uid>\d+)/settings/done/$','translation.views.process_account_settings',name="process_account_settings"),
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

