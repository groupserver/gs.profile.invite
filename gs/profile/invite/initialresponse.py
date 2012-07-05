# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.content.form.form import SiteForm
from gs.group.member.join.interfaces import IGSJoiningUser
from gs.profile.notify.interfaces import IGSNotifyUser
from gs.profile.password.interfaces import IGSPasswordUser
from gs.profile.email.base.emailuser import EmailUser
from gs.profile.email.verify.emailverificationuser import \
  EmailVerificationUser
from interfaces import IGSResponseFields
from invitation import Invitation, FakeInvitation
from audit import Auditor, INVITE_RESPOND, INVITE_RESPOND_ACCEPT, \
    INVITE_RESPOND_DELCINE
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope

class InitialResponseForm(SiteForm):
    label = u'Initial Response'
    pageTemplateFileName = 'browser/templates/initialresponse.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
        self.__groupPrivacy = self.__groupStats = None
    
    @Lazy
    def ctx(self):
        return get_the_actual_instance_from_zope(self.context)
        
    @Lazy
    def form_fields(self):
        retval = form.Fields(IGSResponseFields, render_context=False)
        return retval

    @form.action(label=u'Accept', failure='handle_respond_action_failure')
    def handle_accept(self, action, data):
        if self.invitationId != 'example':
            auditor = Auditor(self.siteInfo, self.userInfo)
            auditor.info(INVITE_RESPOND, self.invitation.groupInfo, 
                self.invitation.adminInfo, INVITE_RESPOND_ACCEPT)

            self.verify_email_address()

            pu = IGSPasswordUser(self.userInfo)
            pu.set_password(data['password1'])

            self.invitation.accept()

            joiningUser = IGSJoiningUser(self.userInfo)
            joiningUser.join(self.groupInfo)

        uri = '%s?welcome=1' % self.groupInfo.relativeURL
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
            auditor = Auditor(self.siteInfo, self.userInfo)
            auditor.info(INVITE_RESPOND, self.invitation.groupInfo, 
                self.invitation.adminInfo, INVITE_RESPOND_DELCINE)
            self.invitation.decline()
            notifiedUser = IGSNotifyUser(self.invitation.adminInfo)
            n_dict = {  'userFn':       self.userInfo.name,
                        'adminFn':      self.invitation.adminInfo.name,
                        'siteName':     self.siteInfo.name,
                        'groupName':    self.invitation.groupInfo.name,
                        'groupURL':     self.invitation.groupInfo.url,}
            notifiedUser.send_notification('invite_join_group_declined',\
                'default', n_dict)
        uri = '/initial_decline.html'
        # --=mpj17=-- When Zope redirects this instance is reloaded and
        #   *then* the redirection occurs. Trying to reload a user that 
        #   no longer exists causes a few issues. So, for now, we do 
        #   nothing.
        #
        #   TODO: A clean-up script will have to find all users who
        #      have declined the initial response and delete them.
        #
        # del(self.context)
        self.request.RESPONSE.redirect(uri)
        
    def handle_respond_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    # Non-Standard methods below this point
    @Lazy
    def invitationId(self):
        retval = self.request.get('form.invitationId', '')
        assert retval, 'Invitation ID not passed to page'
        return retval

    @Lazy
    def invitation(self):
        if self.invitationId == 'example':
            groupId = self.request.form.get('form.groupId', '')
            assert groupId, 'Group ID for the invitation-response '\
                  'preview has not been set.'
            retval = FakeInvitation(self.context, groupId)
        else:
            retval = Invitation(self.context, self.invitationId)
        assert retval
        return retval

    def verify_email_address(self):
        # There better be only one email address.
        emailUser = EmailUser(self.context, self.userInfo)
        email = emailUser.get_addresses()[0]
        # Assuming this will work ;)
        vid = '%s_accept' % self.invitationId
        eu = EmailVerificationUser(self.groupInfo.groupObj, 
                                   self.userInfo, email)
        eu.add_verification_id(vid)
        eu.verify_email(vid)

    @Lazy
    def adminInfo(self):
        return self.invitation.adminInfo

    @Lazy
    def userInfo(self):
        retval = IGSUserInfo(self.context)
        assert retval
        return retval
        
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

