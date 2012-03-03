import os
import sys

def findpath(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),path))

# put the Django project on sys.path
sys.path.insert(0, findpath("../.."))

os.environ["DJANGO_SETTINGS_MODULE"] = "bhagirath.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
