# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from queries import InvitationQuery

class Invitation(object):
    def __init__(self, context, invitationId):
        assert context, 'No context'
        assert invitationId, 'No Invitation ID'
        self.invitationId = invitationId
        self.context = context
        self.__invite = None
        self.__adminInfo = self.__userInfo = self.__groupInfo = None
        
    @property
    def invite(self):
        if self.__invite == None:
            da = self.context.zsqlalchemy
            query = InvitationQuery(da)
            self.__invite = query.get_invitation(self.invitationId, 
                                                    current=False)
            assert self.__invite['invitation_id'] == self.invitationId,\
                'Invitation (%s) not found' % self.invitationId
        return self.__invite
        
    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = createObject('groupserver.UserFromId',
                                            self.context, 
                                            self.invite['user_id'])
        return self.__userInfo

    @property
    def adminInfo(self):
        if self.__adminInfo == None:
            self.__adminInfo = createObject('groupserver.UserFromId',
                                            self.context, 
                                            self.invite['inviting_user_id'])
        return self.__adminInfo

    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            self.__groupInfo = createObject('groupserver.GroupInfo', 
                                            self.context,
                                            self.invite['group_id'])
        return self.__groupInfo

class FakeInvitation(object):
    def __init__(self, context, request):
        assert context, 'No context'
        assert request, 'No request'
        self.invitationId = 'example'
        self.context = context
        self.request = request
        self.__groupInfo = self.__userInfo = None
        
    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = createObject('groupserver.LoggedInUser',
                                            self.context)
        return self.__userInfo

    @property
    def adminInfo(self):
        return self.userInfo

    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            ref = self.request.get('HTTP_REFERER','')
            assert ref, 'This page only works if you follow the link '\
                'from the invitation preview.'
            path = urlparse(ref)[2]
            groupId = path.split('/')[2]
            self.__groupInfo = createObject('groupserver.GroupInfo', 
                                            self.context, groupId)
        return self.__groupInfo

