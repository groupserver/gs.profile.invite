# coding=utf-8
from zope.component import createObject, provideAdapter, adapts
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.interface import Interface, implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.group.member.invite.queries import InvitationQuery
from invitation import Invitation
from interfaces import IGSInvitationListContentProvider

class InvitationList(object):
    implements( IGSInvitationListContentProvider )
    adapts(Interface,
        IDefaultBrowserLayer,
        Interface)
        
    def __init__(self, context, request, view):
        self.__parent__ = self.view = view
        self.__updated = False

        self.context = context
        self.request = request
        self.userInfo = IGSUserInfo(context)
        self.siteInfo = createObject('groupserver.SiteInfo', context)

        self.__invitations = self.__invitationQuery = None
        
    def update(self):
        self.__updated = True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)
        
    #########################################
    # Non standard methods below this point #
    #########################################

    @property
    def invitationQuery(self):
        if self.__invitationQuery == None:
            da = self.context.zsqlalchemy
            assert da, 'No data-adaptor found'
            self.__invitationQuery = InvitationQuery(da)
        return self.__invitationQuery

    @property
    def invitations(self):
        if self.__invitations == None:
            gci = self.invitationQuery.get_current_invitiations_for_site
            self.__invitations = [Invitation(self.context, i['invitation_id']) 
                for i in gci(self.siteInfo.id, self.userInfo.id)]
        return self.__invitations

