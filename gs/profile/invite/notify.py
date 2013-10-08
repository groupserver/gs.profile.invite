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
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.profile.notify.sender import MessageSender
UTF8 = 'utf-8'


class DeclineNotifier(object):
    textTemplateName = 'gs-profile-invite-decline.txt'
    htmlTemplateName = 'gs-profile-invite-decline.html'

    def __init__(self, user, request):
        self.context = self.user = user
        self.request = request

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, adminInfo, userInfo, groupInfo):
        s = u'Invitation to {0} declined'
        subject = s.format(groupInfo.name).encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                    groupInfo=groupInfo)
        html = self.htmlTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                    groupInfo=groupInfo)
        ms = MessageSender(self.context, adminInfo)
        ms.send_message(subject, text, html)


class AcceptNotifier(DeclineNotifier):
    textTemplateName = 'gs-profile-invite-accept.txt'
    htmlTemplateName = 'gs-profile-invite-accept.html'

    def notify(self, adminInfo, userInfo, groupInfo):
        s = u'Invitation to {0} accepted'
        subject = s.format(groupInfo.name).encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                    groupInfo=groupInfo)
        html = self.htmlTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                    groupInfo=groupInfo)
        ms = MessageSender(self.context, adminInfo)
        ms.send_message(subject, text, html)
