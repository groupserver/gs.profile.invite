# coding=utf-8
from urllib import quote
from zope.component import createObject
from Products.Five import BrowserView

class InvitationAccepted(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.groupInfo = None
    
    @property
    def userInfo(self):
        retval = None
        return retval
    
    @property
    def profileLogin(self):
        retval = 'Fix Me'
        return retval
          
    @property
    def uri(self):
        retval = 'Fix Me'
        return retval

    def quote(self, msg):
        assert msg
        retval = quote(msg)
        assert retval
        return retval

