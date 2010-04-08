# coding=utf-8
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.GSGroupMember.utils import inform_ptn_coach_of_join
from Products.GSProfile.set_password import SetPasswordForm, set_password
from interfaces import IGSSetPasswordAdminInvite

class SetPasswordAdminInviteForm(SetPasswordForm):
    form_fields = form.Fields(IGSSetPasswordAdminInvite)
    label = u'Join'
    pageTemplateFileName = 'browser/templates/set_password_invite.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self):
        self.__groupInfo = None
        
    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            # TODO: look up the invitation, return the group
            pass

    @form.action(label=u'Join', failure='handle_join_action_failure')
    def handle_join(self, action, data):
        assert self.context
        assert self.form_fields
        assert action
        assert data

        loggedInUser = createObject('groupserver.LoggedInUser',
                                    self.context)
        assert not(loggedInUser.anonymous), 'Not logged in'
        user = loggedInUser.user
        
        set_password(user, data['password1'])

        # Add User to the Group
        userGroup = '%s_member' % self.groupInfo.get_id()
        # TODO: why not join_group(user, self.groupInfo)?
        if userGroup not in user.getGroups():
            user.add_groupWithNotification(userGroup)
        assert userGroup in user.getGroups()
        user.remove_invitations()
        user.verify_emailAddress(data['invitationId'])

        ptnCoachId = self.groupInfo.get_property('ptn_coach_id', '')
        if ptnCoachId:
            ptnCoachInfo = createObject('groupserver.UserFromId', 
                                        self.context, ptnCoachId)
            inform_ptn_coach_of_join(ptnCoachInfo, self.userInfo, self.groupInfo)
        
        uri = '%s?welcome=1' % self.groupInfo.get_url()
        m = u'SetPasswordAdminJoinForm: redirecting user to %s' % uri
        log.info(m)
        return self.request.RESPONSE.redirect(uri)

    def handle_join_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

