# coding=utf-8
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
            query = InvitationQuery(self.context, da)
            self.__invite = query.get_invitation(invitationId, current=False)
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

