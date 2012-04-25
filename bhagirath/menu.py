"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'bhagirath.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from admin_tools.menu.items import MenuItem

from bhagirath.translation.models import *

        
class CustomMenu(Menu):
    """
    Custom Menu for bhagirath admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            
            items.MenuItem('Current Activity',
                children=[
                    items.MenuItem('Logged-in users', '/current_activity/active_users/'),
                    items.MenuItem('Current translations', '/current_activity/current_translations/'),
                    items.MenuItem('Translations with maximum hops', '/current_activity/translations_max_hops/'),
                    items.MenuItem('Translations with minimum hops', '/current_activity/translations_min_hops/'),
                    items.MenuItem('Total sentences translated', '/current_activity/total_translations/'),
                    items.MenuItem('Average translation rate', '/current_activity/avg_translation_rate/'),
                    items.MenuItem('Average convergence rate', '/current_activity/avg_convergence_rate/'),
                    #items.MenuItem('Microtask similarity score', '/current_activity/microtask_similarity_score/')
                ]
            ),
                           
            items.MenuItem('Background Tasks',
                children=[
                    items.MenuItem('Populate Subtask', '/background_task/populate_subtask/'),
                    items.MenuItem('Populate StaticMicrotask', '/background_task/populate_staticmicrotask/'),
                    items.MenuItem('Populate Microtask', '/background_task/populate_microtask/'),
                    items.MenuItem('Unassign Microtask', '/background_task/unassign_microtask/'),
                    items.MenuItem('Upload Priviledge', '/background_task/upload_priviledge/'),
                    items.MenuItem('Update Weekly Leaderboard', '/background_task/update_weekly_leaderboard/'),
                    items.MenuItem('Update Overall Leaderboard', '/background_task/update_overall_leaderboard/'),
                    items.MenuItem('Update Statistics Counter', '/background_task/update_statistics_counter/'),
                    items.MenuItem('Document Stability', '/background_task/document_stability/'),
                    items.MenuItem('Reputation Score', '/background_task/reputation_score/'),
                    items.MenuItem('Assign Rank', '/background_task/assign_rank/')
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        request = context['request']
        return super(CustomMenu, self).init_with_context(context)