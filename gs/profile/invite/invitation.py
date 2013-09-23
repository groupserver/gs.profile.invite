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
from zope.component import createObject
from gs.group.member.invite.base.queries import InvitationQuery


class Invitation(object):
    def __init__(self, context, invitationId):
        if not context:
                raise ValueError('context is {0}'.format(type(context)))
        self.context = context

        if not invitationId:
            raise ValueError('invitationId is {0}'.format(type(invitationId)))
        self.invitationId = invitationId

    @Lazy
    def query(self):
        retval = InvitationQuery()
        assert retval
        return retval

    @Lazy
    def invite(self):
        retval = self.query.get_invitation(self.invitationId, current=False)
        if retval['invitation_id'] != self.invitationId:
            raise KeyError(self.invitationId)
        assert retval, 'invite is {0}'.format(type(retval))
        return retval

    @Lazy
    def siteObj(self):
        retval = getattr(self.context.Content, self.invite['site_id'])
        assert retval, 'No site object found %s' % self.invite['site_id']
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.siteObj)
        return retval

    @Lazy
    def userInfo(self):
        retval = createObject('groupserver.UserFromId', self.siteObj,
                                self.invite['user_id'])
        assert retval
        return retval

    @Lazy
    def adminInfo(self):
        retval = createObject('groupserver.UserFromId', self.siteObj,
                                self.invite['inviting_user_id'])
        assert retval
        return retval

    @Lazy
    def groupInfo(self):
        assert self.invite['group_id']
        retval = createObject('groupserver.GroupInfo', self.siteObj,
                                self.invite['group_id'])
        assert retval
        return retval

    def accept(self):
        siteId = self.groupInfo.siteInfo.id
        groupId = self.groupInfo.id
        userId = self.userInfo.id
        self.query.accept_invitation(siteId, groupId, userId)

    def decline(self):
        siteId = self.groupInfo.siteInfo.id
        groupId = self.groupInfo.id
        userId = self.userInfo.id
        self.query.decline_invitation(siteId, groupId, userId)


class FakeInvitation(object):
    def __init__(self, context, groupId):
        if not context:
                raise ValueError('context is {0}'.format(type(context)))
        self.context = context

        if not groupId:
            raise ValueError('groupId is {0}'.format(type(groupId)))
        self.groupId = groupId

    @Lazy
    def userInfo(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    @Lazy
    def adminInfo(self):
        return self.userInfo

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context,
                                self.groupId)
        return retval

    def accept(self):
        raise NotImplemented

    def decline(self):
        raise NotImplemented
