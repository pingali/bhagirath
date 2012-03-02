from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import re 
import dateutil.parser as dparser
from datetime import datetime
import traceback 
import time 
import sys
import logging 
import subprocess

log = logging.getLogger("LPGDB")

#=================================================================
# Prevent sql commands from being printed out for this section...
from django.db.backends import BaseDatabaseWrapper
from django.db.backends.util import CursorWrapper

if settings.DEBUG:
    BaseDatabaseWrapper.make_debug_cursor = \
        lambda self, cursor: CursorWrapper(cursor, self)
#==================================================================

from bhagirath.translation_interface.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--show-model',
                    action='store',
                    dest='show_model',
                    default="Language",
                    help='Show model objects (default=Language)'),
        make_option('--db',
                    action='store',
                    dest='db',
                    default='default',
                    help='Database setting in settings.py (default=default)'),
        )

    help = 'Show translation data'

    def handle(self, **options):
        
        db_setting = options['db']
        if (not settings.DATABASES.has_key(db_setting)):
            #print "Unknown database %s " % dbname
            sys.exit(1) 
            return 
        db = settings.DATABASES[db_setting] 
        dbname = db['NAME']
        dbuser = db['USER']
        dbpass = db['PASSWORD']
        
        if options['show_model'] != None:
            modelname = options['show_model']            
            count = eval('%s.objects.all().count()' % modelname)
            print "Found %d %s objects" % (count, modelname)
            objs = eval('%s.objects.all().order_by("-id")[:5]' % modelname)
            print "Last few table entries for %s" % modelname
            for o in objs: 
                x = vars(o)
                del x['_state'] 
                print x

