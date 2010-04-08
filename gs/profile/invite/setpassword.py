# coding=utf-8
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.GSGroupMember.utils import inform_ptn_coach_of_join
from Products.GSProfile.set_password import SetPasswordForm, set_password
from interfaces import IGSSetPasswordAdminInvite
from queries import InvitationQuery
from invitation import Invitation
from Products.GSGroupMember.groupmembership import join_group

class SetPasswordAdminInviteForm(SetPasswordForm):
    form_fields = form.Fields(IGSSetPasswordAdminInvite)
    label = u'Join'
    pageTemplateFileName = 'browser/templates/set_password_invite.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self):
        self.__groupInfo = self.__invitation = None

    @form.action(label=u'Join', failure='handle_join_action_failure')
    def handle_join(self, action, data):
        assert self.context
        assert self.form_fields
        assert action
        assert data

        user = self.userInfo.user        
        set_password(user, data['password1'])
        
        join_group(user, self.invitation.groupInfo)
        user.remove_invitations() # --=mpj17=-- NO!
        user.verify_emailAddress(data['invitationId']) # --=mpj17=-- Eh?
        
        uri = '%s?welcome=1' % self.groupInfo.get_url()
        m = u'SetPasswordAdminJoinForm: redirecting user to %s' % uri
        log.info(m)
        return self.request.RESPONSE.redirect(uri)

    def handle_join_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = createObject('groupserver.LoggedInUser',
                                self.context)
            assert not(self.__userInfo.anonymous), 'Not logged in'
        return self.__userInfo
        
    @property
    def invitation(self):
        if self.__invitation == None:
            da = self.context.zsqlalchemy
            query = InvitationQuery(self.context, da)
            inviteId = query.get_only_invitation(self.userInfo)['invitation_id']
            assert inviteId, 'Not invited!'
            self.__invitation = Invitation(self.context, inviteId)
        return self.__invitation

