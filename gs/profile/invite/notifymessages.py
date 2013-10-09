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
from textwrap import fill
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import GroupEmail
UTF8 = 'utf-8'


class NotifyAcceptMessage(GroupEmail):
    subject = u'Invitation accepted'

    @Lazy
    def supportEmail(self):
        m = u'Hi!\n\nI am an administrator of the group {0}\n    {1}\nand...'
        msg = m.format(self.groupInfo.name, self.groupInfo.url)
        sub = quote(self.subject)
        retval = 'mailto:%s?Subject=%s&body=%s' % \
            (self.siteInfo.get_support_email(), sub, quote(msg.encode(UTF8)))
        return retval


class NotifyAcceptMessageText(NotifyAcceptMessage):
    def __init__(self, context, request):
        super(NotifyAcceptMessageText, self).__init__(context, request)

        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'gs-profile-invite-accept.txt'
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)

    def fill(self, mesg):
        print '\n\n{0}\n\n'.format(mesg)
        retval = fill(mesg)
        print '\n\n{0}\n\n'.format(retval)
        return retval


class NotifyDeclineMessage(NotifyAcceptMessage):
    subject = u'Invitation declined'


class NotifyDeclineMessageText(NotifyDeclineMessage):
    def __init__(self, context, request):
        super(NotifyDeclineMessageText, self).__init__(context, request)

        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'gs-profile-invite-decline.txt'
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)

    def fill(self, mesg):
        retval = fill(mesg)
        return retval
