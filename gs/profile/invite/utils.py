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
from gs.group.member.join import NotifyNewMember, NotifyAdmin
from gs.group.member.join.interfaces import IGSJoiningUser
from .notify import AcceptNotifier


def join_group(invitation, request):
    joiningUser = IGSJoiningUser(invitation.userInfo)
    joiningUser.silent_join(invitation.groupInfo)

    # Send the Welcome to the new member
    groupCtx = invitation.groupInfo.groupObj
    notifier = NotifyNewMember(groupCtx, request)
    notifier.notify(invitation.userInfo)

    # Send the Invitation Accepted to the person who issued the invite
    inviterNotifier = AcceptNotifier(groupCtx, request)
    inviterNotifier .notify(invitation.adminInfo, invitation.userInfo,
                            invitation.groupInfo)

    # Send the New Member to all the other admins
    adminNotifier = NotifyAdmin(groupCtx, request)
    for adminInfo in invitation.groupInfo.group_admins:
        if adminInfo.id != invitation.adminInfo.id:
            adminNotifier.notify(adminInfo, invitation.userInfo)
