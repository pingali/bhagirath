# Django settings for bhagirath project.
import os
import sys
import logging

#####################################
# Helper functions 
#####################################

def findpath(path):
    """
     This function provides absolute path of file specified.
    """ 
    parent_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(parent_dir,path))

def findglobalpath(path):
    """
     This function provides absolute path of file specified on the 
     deployed server
    """ 
    this_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(this_dir,"../../.."))
    return os.path.abspath(os.path.join(root_dir,path))

def is_production_server(): 
    return (findpath(".").find('releases') > 0)

# Is this production deployment? 
if is_production_server(): 
    dbfile = findglobalpath('shared/bhagirath.db') 
    admin_media_path = findglobalpath('lib/python2.7/site-packages/admin_tools/media/admin_tools')
    logfile = findglobalpath('logs/bhagirath.log')
else:    
    dbfile = findpath('bhagirath.db') 
    admin_media_path = '/usr/local/lib/python2.7/dist-packages/admin_tools/media/admin_tools'
    logfile = findpath('bhagirath.log')


#####################################
# Main configuration 
#####################################

if is_production_server(): 
    DEBUG = False
else: 
    DEBUG = True 

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': dbfile,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_CHARSET': 'utf-8',
        'DEFAULT_CHARSET': 'utf-8',
        'default-collation':'utf8_general_ci',
        'default-character-set':'utf8'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"


MEDIA_ROOT = findpath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL ='/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '' 

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    findpath('static'),
    admin_media_path, 
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')jv33#l$85iq=ni*43%5z52i482&&ykh$+etg^ex)$n)i-7qp-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

CRON_CLASSES = (
    'bhagirath.translation.cron.PopulateSubtaskCronJob',
    'bhagirath.translation.cron.PopulateStaticMicrotaskCronJob',
    'bhagirath.translation.cron.PopulateMicrotaskCronJob',
    'bhagirath.translation.cron.UnassignMicrotaskCronJob',
    'bhagirath.translation.cron.UploadPriviledgeCronJob',
    'bhagirath.translation.cron.UpdateLeaderBoardCronJob',
    'bhagirath.translation.cron.UpdateStatisticsCounterCronJob',
    'bhagirath.translation.cron.DocumentStabilityCronJob',
    'bhagirath.translation.cron.ReputationScoreCronJob'
)

ROOT_URLCONF = 'bhagirath.urls'

TEMPLATE_DIRS = (
    findpath('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    # required by django-admin-tools
    'django.core.context_processors.request',
)

ADMIN_TOOLS_MENU = 'bhagirath.menu.CustomMenu'

ADMIN_TOOLS_INDEX_DASHBOARD = 'bhagirath.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'bhagirath.dashboard.CustomAppIndexDashboard'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',                  
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_basic_feedback', 
    'django_cron',
    'captcha',
    'bhagirath.translation',
    'south'
)

FIXTURE_DIRS = (
   findpath('fixtures'),
)

AUTH_PROFILE_MODULE = 'bhagirath.UserProfile'

##############################################################
# CAPTCHA SETTINGS 
##############################################################
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_FONT_SIZE = 30
CAPTCHA_LETTER_ROTATION = None
CAPTCHA_BACKGROUND_COLOR = "#ffffff"
CAPTCHA_FOREGROUND_COLOR = "#000000"
CAPTCHA_TIMEOUT = 10
CAPTCHA_OUTPUT_FORMAT = u'%(image)s %(hidden_field)s %(text_field)s' 

##############################################################
# Logging
##############################################################
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s',
                    filename= logfile, 
                    filemode= 'a+',
                    handlers=[handler],
                    )

#
## A sample logging configuration. The only tangible logging
## performed by this configuration is to send an email to
## the site admins on every HTTP 500 error.
## See http://docs.djangoproject.com/en/dev/topics/logging for
## more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
#
