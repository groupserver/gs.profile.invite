# coding=utf-8
from urllib import quote
from zope.component import createObject
from Products.Five import BrowserView
from Products.CustomUserFolder.interfaces import IGSUserInfo
from invitation import Invitation

class InvitationAccepted(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.__invitation = None
        self.__groupInfo = None
        self.__userInfo = None
        
    @property
    def invitation(self):
        if self.__invitation == None:
            invitationId = self.request.get('i', '')
            self.__invitation = Invitation(self.context, invitationId)
            # Security issue
            assert self.__invitation.userId == self.userInfo.id, \
                '"%s" Viewing the invitation of "%s"' %\
                (self.userInfo.id, self.__invitation.userId)
        return self.__invitation
    
    @property
    def groupInfo(self):
        if self.__groupInfo == None
            self.__groupInfo = createObject('groupserver.GroupInfo', 
                self.context, self.invitation.groupId)
        return self.__groupInfo
    
    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = IGSUserInfo(self.context)
        assert self.__userInfo
        assert not(self.__userInfo.anonymous)
        return self.__userInfo
    
    @property
    def profileLogin(self):
        retval = '/login.html?came_from=%s' % quote(self.userInfo.uri)
        assert retval
        return retval
          
    @property
    def uri(self):
        retval = self.request.get('r', '')
        return retval

    def quote(self, msg):
        assert msg
        retval = quote(msg)
        assert retval
        return retval

