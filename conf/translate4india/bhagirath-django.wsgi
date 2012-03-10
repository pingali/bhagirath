import os
import sys
from django.core.handlers.wsgi import WSGIHandler

def findpath(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),path))

# put the Django project on sys.path
sys.path.insert(0, findpath("../.."))
sys.path.insert(0, findpath("../../bhagirath"))

os.environ["DJANGO_SETTINGS_MODULE"] = "bhagirath.settings"

_application = WSGIHandler()

def application(environ, start_response):
    # trick django into thinking proxied traffic is coming in via HTTPS
    # HTTP_X_FORWARDED_SSL is used on WebFaction
    if environ.get("HTTP_X_FORWARDED_PROTOCOL") == "https" or \
       environ.get("HTTP_X_FORWARDED_SSL") == "on":
        environ["wsgi.url_scheme"] = "https"
	print "FOUND HTTPS in django.wsgi" 
    return _application(environ, start_response)
