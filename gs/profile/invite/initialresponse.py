# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from zope.component import createObject
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSGroup.changebasicprivacy import radio_widget
from gs.profile.notify.interfaces import IGSNotifyUser
from gs.profile.notify.adressee import Addressee, SupportAddressee
from interfaces import IGSResponseFields
from invitation import Invitation, FakeInvitation
from utils import send_add_user_notification
from audit import Auditor, INVITE_RESPOND

class InitialResponseForm(PageForm):
    label = u'Intial Response'
    pageTemplateFileName = 'browser/templates/initialresponse.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.siteInfo = createObject('groupserver.SiteInfo', self.context)
        
        self.__formFields = self.__invitation = self.__invitationId = None
        self.__groupPrivacy = self.__groupStats = None
        
    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(IGSResponseFields, 
                                            render_context=False)
        return self.__formFields

    @form.action(label=u'Accept', failure='handle_respond_action_failure')
    def handle_accept(self, action, data):
        pass
        
    @form.action(label=u'Decline', failure='handle_respond_action_failure')
    def handle_decline(self, action, data):
        pass

    def handle_respond_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
                self.status = u'<p>There rare errors:</p>'
            
    # Non-Standard methods below this point
    @property
    def invitationId(self):
        if self.__invitationId == None:
            self.__invitiationId = self.request.get('form.invitationId', '')
            assert self.__invitiationId, 'Invitation ID not passed to page'
        return self.__invitiationId

    @property
    def invitation(self):
        if self.__invitation == None:
            # --=mpj17=-- Sometimes Zope acquisition can be a hideous
            # pain in the arse. This is one of those times. For whatever
            # reason, self.context gets all wrapped up in some voodoo 
            # to do with "Products.Five.metaclass". The "aq_self" is
            # required to exorcise the Dark Magiks and to allow the code
            # to operate without spewing errors about the site-instance
            # being None.
            if self.invitationId == 'example':
                i = FakeInvitation(self.context.aq_self, self.request)
            else:
                i = Invitation(self.context.aq_self, self.invitationId)
            self.__invitation = i
        return self.__invitation

    @property
    def adminInfo(self):
        return self.invitation.adminInfo

    @property
    def userInfo(self):
        return self.invitation.userInfo

    @property
    def groupInfo(self):
        return self.invitation.groupInfo

    @property
    def groupPrivacy(self):
        return self.__groupPrivacy

    @property
    def groupStats(self):
        return self.__groupStats

