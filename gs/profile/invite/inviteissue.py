# coding=utf-8
from zope.component import createObject
from Products.GSContent.view import GSContentView
from invitation import Invitation

class IssueView(GSContentView):
    def __init__(self, context, request):
        GSContentView.__init__(self, context, request)
        invitationId = request.get('form.invitationId', '')
        self.invitation = None
        if invitationId:
            self.invitation = Invitation(context, invitationId)
        self.loggedInUser = createObject('groupserver.LoggedInUser',
                                            self.context)

