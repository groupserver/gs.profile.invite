# -*- coding: utf-8 -*-
from urllib import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.profile.page import ProfilePage
from invitation import Invitation


class InvitationAccepted(ProfilePage):

    def __init__(self, profile, request):
        super(InvitationAccepted, self).__init__(profile, request)

    @Lazy
    def invitation(self):
        invitationId = self.request.get('i', '')
        retval = Invitation(self.context, invitationId)
        # FIXME: riase a security issue
        assert retval.userId == self.userInfo.id, \
            '"%s" Viewing the invitation of "%s"' %\
            (self.userInfo.id, self.__invitation.userId)
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context,
                                self.invitation.groupId)
        return retval

    @Lazy
    def profileLogin(self):
        retval = '/login.html?came_from=%s' % quote(self.userInfo.uri)
        assert retval
        return retval

    @Lazy
    def uri(self):
        retval = self.request.get('r', '')
        return retval

    def quote(self, msg):
        assert msg
        retval = quote(msg)
        assert retval
        return retval
