# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.component import adapts
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.interface import Interface, implements
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from gs.group.member.invite.base.queries import InvitationQuery
from gs.profile.base import ProfileContentProvider
from invitation import Invitation
from interfaces import IGSInvitationListContentProvider


class InvitationList(ProfileContentProvider):
    implements(IGSInvitationListContentProvider)
    adapts(Interface,
        IDefaultBrowserLayer,
        Interface)

    def __init__(self, profile, request, view):
        super(InvitationList, self).__init__(profile, request, view)
        self.__updated = False

    def update(self):
        self.__updated = True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)

    #########################################
    # Non standard methods below this point #
    #########################################

    @Lazy
    def invitationQuery(self):
        retval = InvitationQuery()
        return retval

    @Lazy
    def invitations(self):
        gci = self.invitationQuery.get_current_invitiations_for_site
        retval = [Invitation(self.context, i['invitation_id'])
                    for i in gci(self.siteInfo.id, self.userInfo.id)]
        return retval
