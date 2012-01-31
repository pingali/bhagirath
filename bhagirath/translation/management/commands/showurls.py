from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import sys

from bhagirath import urls

def show_urls(urllist, depth=0):
    for entry in urllist:
        print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        )

    help = 'Show URLs'

    def handle(self, **options):
        show_urls(urls.urlpatterns)

