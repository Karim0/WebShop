from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))
        self.children.append(modules.RecentActions(
            title='Django CMS recent actions',
            include_list=('cms.page', 'cms.cmsplugin',)
        ))
