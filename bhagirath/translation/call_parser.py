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
from django.db.backends.util import *
from django.db.backends.util import CursorWrapper
from bhagirath.translation.subtask_parser import subtaskParser
from bhagirath.translation.microtask_parser import microtaskParser
if settings.DEBUG:
    BaseDatabaseWrapper.make_debug_cursor = \
        lambda self, cursor: CursorWrapper(cursor, self)
#==================================================================

from bhagirath.translation.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--show-model',
                    action='store',
                    dest='show_model',
                    default="Master_Language",
                    help='Show model objects (default=Master_Language)'),
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
           # print "Unknown database %s " % dbname
            sys.exit(1) 
            return 
        db = settings.DATABASES[db_setting] 
        dbname = db['NAME']
        dbuser = db['USER']
        dbpass = db['PASSWORD']
        

subtaskParser('Wordnet.html') 
#        microtaskParser()
       

