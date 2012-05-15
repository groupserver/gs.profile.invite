# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from gs.group.member.invite.base.queries import InvitationQuery

class Invitation(object):
    def __init__(self, context, invitationId):
        assert context, 'No context'
        assert invitationId, 'No Invitation ID'
        self.invitationId = invitationId
        self.context = context
        self.__query = None
        self.__adminInfo = self.__siteObj = self.__siteInfo = None
        self.__groupInfo = self.__userInfo = self.__invite = None
    
    @property
    def query(self):
        if self.__query == None:
            da = self.context.zsqlalchemy
            self.__query = InvitationQuery(da)
            assert self.__query
        return self.__query
    
    @property
    def invite(self):
        if self.__invite == None:
            self.__invite = self.query.get_invitation(self.invitationId, 
                                                        current=False)
            if self.__invite['invitation_id'] != self.invitationId:
                raise KeyError(self.invitationId)
        assert self.__invite
        return self.__invite
    
    @property
    def siteObj(self):
        if self.__siteObj == None:
            self.__siteObj = getattr(self.context.Content, \
                                self.invite['site_id'])
        assert self.__siteObj, 'No site object found %s' % \
            self.invite['site_id']
        return self.__siteObj
    
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo', 
                                            self.siteObj)
        return self.__siteInfo
    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = createObject('groupserver.UserFromId',
                                            self.siteObj, 
                                            self.invite['user_id'])
        assert self.__userInfo
        return self.__userInfo

    @property
    def adminInfo(self):
        if self.__adminInfo == None:
            self.__adminInfo = createObject('groupserver.UserFromId',
                                            self.siteObj, 
                                            self.invite['inviting_user_id'])
        assert self.__adminInfo
        return self.__adminInfo

    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            assert self.invite['group_id']
            self.__groupInfo = createObject('groupserver.GroupInfo', 
                                            self.siteObj,
                                            self.invite['group_id'])
        assert self.__groupInfo
        return self.__groupInfo

    def accept(self):
        siteId = self.groupInfo.siteInfo.id
        groupId = self.groupInfo.id
        userId = self.userInfo.id
        self.query.accept_invitation(siteId, groupId, userId)
        
    def decline(self):
        siteId = self.groupInfo.siteInfo.id
        groupId = self.groupInfo.id
        userId = self.userInfo.id
        self.query.decline_invitation(siteId, groupId, userId)

class FakeInvitation(object):
    def __init__(self, context, groupId):
        assert context, 'No context'
        assert groupId, 'No groupId'
        self.invitationId = 'example'
        self.context = context
        self.groupId = groupId
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
            self.__groupInfo = createObject('groupserver.GroupInfo', 
                                            self.context, self.groupId)
        return self.__groupInfo

    def accept(self):
        raise NotImplemented
        
    def decline(self):
        raise NotImplemented

