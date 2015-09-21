# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, print_function, unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import GroupEmail, TextMixin
UTF8 = 'utf-8'


class NotifyAcceptMessage(GroupEmail):
    subject = 'Invitation accepted'

    @Lazy
    def supportEmail(self):
        m = 'Hi!\n\nI am an administrator of the group {0}\n    {1}\nand...'
        msg = m.format(self.groupInfo.name, self.groupInfo.url)
        sub = self.subject
        retval = self.mailto(self.siteInfo.get_support_email(), sub, msg)
        return retval


class NotifyAcceptMessageText(NotifyAcceptMessage, TextMixin):
    def __init__(self, context, request):
        super(NotifyAcceptMessageText, self).__init__(context, request)
        filename = 'gs-profile-invite-accept-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)


class NotifyDeclineMessage(NotifyAcceptMessage):
    subject = 'Invitation declined'


class NotifyDeclineMessageText(NotifyDeclineMessage, TextMixin):
    def __init__(self, context, request):
        super(NotifyDeclineMessageText, self).__init__(context, request)
        filename = 'gs-profile-invite-decline-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)
