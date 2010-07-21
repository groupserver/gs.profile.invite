# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from zope.component import createObject
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
try:
    from five.formlib.formbase import PageForm
except ImportError:
    from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSProfile.set_password import set_password
from gs.group.member.join.interfaces import IGSJoiningUser
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
        self.__siteInfo = None
        self.__formFields = self.__invitation = self.__invitationId = None
        self.__groupPrivacy = self.__groupStats = self.__userInfo = None
        
    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(IGSResponseFields, 
                                            render_context=False)
        return self.__formFields

    @form.action(label=u'Accept', failure='handle_respond_action_failure')
    def handle_accept(self, action, data):
        if self.invitationId != 'example':
            self.verify_email_address()
            set_password(self.userInfo.user, data['password1'])
            self.invitation.accept()
            joiningUser = IGSJoiningUser(self.userInfo)
            joiningUser.join(self.groupInfo)
        uri = '%s?welcome=1' % self.groupInfo.url
        self.request.RESPONSE.redirect(uri)
        
    @form.action(label=u'Decline', failure='handle_respond_action_failure')
    def handle_decline(self, action, data):
        if self.invitationId != 'example':
            # --=mpj17=-- We cannot delete the user-instance at this 
            #   stage. This method will return, so it requires the 
            #   context (the user) to still be there. If we delete the
            #   user instance we get a Not Found error. The 
            #   initial_decline.html page notes that the user-instance
            #   will be deleted later on.
            #self.context.acl_users.manage_delObjects([self.userInfo.id])
            self.invitation.decline()
            # TODO: Tell someone
        uri = '/initial_decline.html'
        self.request.RESPONSE.redirect(uri)
        
    def handle_respond_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    def notify_people(self):
        # TODO: Tell the admin
        pass
    
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
                groupId = self.request.form.get('form.groupId', '')
                assert groupId, 'Group ID for the invitation-response '\
                  'preview has not been set.'
                i = FakeInvitation(self.context.aq_self, groupId)
            else:
                i = Invitation(self.context.aq_self, self.invitationId)
            self.__invitation = i
        return self.__invitation

    def verify_email_address(self):
        # There better be only one email address.
        email  = self.userInfo.user.get_emailAddresses()[0]
        # Assuming this will work ;)
        vid = '%s_accept' % self.invitationId
        self.userInfo.user.add_emailAddressVerification(vid, email)
        self.userInfo.user.verify_emailAddress(vid)

    @property
    def adminInfo(self):
        return self.invitation.adminInfo

    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = IGSUserInfo(self.context.aq_self)
        assert self.__userInfo
        return self.__userInfo
        
    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = createObject('groupserver.SiteInfo', 
                                self.context.aq_self)
        assert self.__siteInfo
        return self.__siteInfo

    @property
    def groupInfo(self):
        retval = self.invitation.groupInfo
        assert retval, 'No group'
        return retval

    @property
    def groupPrivacy(self):
        return self.__groupPrivacy

    @property
    def groupStats(self):
        return self.__groupStats

