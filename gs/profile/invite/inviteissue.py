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
from __future__ import absolute_import
from urllib import quote
from zope.component import createObject
from Products.GSContent.view import GSContentView
from .invitation import Invitation


class IssueView(GSContentView):
    def __init__(self, context, request):
        GSContentView.__init__(self, context, request)
        self.invitationId = request.get('form.invitationId', '')
        self.invitation = None
        if self.invitationId:
            self.invitation = Invitation(context, self.invitationId)
        self.loggedInUser = createObject('groupserver.LoggedInUser',
                                            self.context)

    def quote(self, msg):
        assert msg
        retval = quote(msg)
        assert retval
        return retval
