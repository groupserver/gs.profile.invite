# -*- coding: utf-8 -*-
from urllib import quote
from zope.component import createObject
from Products.GSContent.view import GSContentView
from invitation import Invitation


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
