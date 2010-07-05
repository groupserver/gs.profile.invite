# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from invitation import Invitation

class GSInvitationResponseRedirect(GSRedirectBase):
    def __call__(self):
        # TODO: Audit
        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            
            if (invitationId == 'example'):
                userInfo = createObject('groupserver.LoggedInUser',
                                        self.context)
                ref = self.request.get('HTTP_REFERER','')
                assert ref, 'This page only works if you follow the link '\
                    'from the invitation preview.'
                path = urlparse(ref)[2]
                groupId = path.split('/')[2]
                uri = '%s/intial_response.html?form.invitationId=example&form.groupId=%s' %\
                  (userInfo.url, groupId)
            else: # Not an example
                invitation = Invitation(self.context, invitationId)
                try:
                    hadResponse = invitation.invite['response_date'] !=  None
                except KeyError, err:
                    hadResponse = False
                    inviteExists = False
                else:
                    inviteExists = True

                if inviteExists and hadResponse:
                    uri = '/invitation-responded.html?form.invitationId=%s' %\
                        invitationId
                elif inviteExists and not(hadResponse):
                    login(self.context, invitation.userInfo.user)
                    if invitation.invite['initial_invite']:
                        # Go to the initial response page, so
                        #   the new user can set a password (and verify
                        #   his or her email address).
                        uri = '%s/intial_response.html?form.invitationId=%s'%\
                              (invitation.userInfo.url, invitationId)
                    else:
                        # If the user is already a member of a group 
                        #   (any group on any site) then we should go to
                        #   the normal Response page.
                        uri = '%s/invitations_respond.html' % \
                                invitation.userInfo.url
                else: # Invitation does not exist
                    uri = '/invite-not-found.html'
        else: # Verification ID not specified
            uri = '/invite-no-id.html'
        assert uri
        assert type(uri) == str
        return self.request.RESPONSE.redirect(uri)

