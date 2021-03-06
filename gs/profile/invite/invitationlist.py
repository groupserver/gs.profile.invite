# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.cachedescriptors.property import Lazy
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from gs.group.member.invite.base.queries import InvitationQuery
from gs.profile.base import ProfileContentProvider
from invitation import Invitation


class InvitationList(ProfileContentProvider):

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
