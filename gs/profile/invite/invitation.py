# coding=utf-8
from Products.GSProfile.queries import InvitationQuery

class Invitation(self):
    def __init__(self, context, invitationId):
        assert context, 'No context'
        assert invitationId, 'No Invitation ID'
        self.invitationId = invitationId
        self.context = context
        self.__invite = None
        
    @property
    def invite(self):
        if self.__invite == None:
            da = self.context.zsqlalchemy
            query = InvitationQuery(self.context, da)
            self.__invite = query.get_invitation(invitationId)
        return self.__invite
        
    def userId(self):
        return self.invite['user_id']

    def invitingUserId(self):
        return self.invite['inviting_user_id']

    def groupId(self):
        return self.invite('group_id')

