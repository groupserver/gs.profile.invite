# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from invitation import Invitation

class GSInvitationResponseRedirect(GSRedirectBase):
    def __call__(self):
        
        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            
            if (invitationId == 'example'):
                userInfo = createObject('groupserver.LoggedInUser',
                                        self.context.aq_self)
                ref = self.request.get('HTTP_REFERER','')
                assert ref, 'This page only works if you follow the link '\
                    'from the invitation preview.'
                path = urlparse(ref)[2]
                groupId = path.split('/')[2]
                uri = '%s/intial_response.html?form.invitationId=example&form.groupId=%s' %\
                  (userInfo.url, groupId)
            else: # Not an example
                invitation = Invitation(self.context.aq_self, invitationId)
                try:
                    hadResponse = \
                        invitation.invite['response_date'] !=  None
                    invitationWithdrawn = \
                        invitation.invite['withdrawn_date'] !=  None
                except KeyError, err:
                    hadResponse = inviteExists = invitationWithdrawn = False
                else:
                    inviteExists = True

                if inviteExists and hadResponse:
                    uri = '/invitation-responded.html?form.invitationId=%s' %\
                            invitationId
                elif inviteExists and not(hadResponse) and not(invitationWithdrawn):
                    # --=mpj17=-- Only ever log in when responding
                    login(self.context.aq_self, invitation.userInfo.user)
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
                elif inviteExists and invitationWithdrawn:
                    # The invitation has been withdrawn
                    uri = '/invitation-withdrawn.html?form.invitationId=%s' %\
                            invitationId
                else: # Invitation does not exist
                    uri = '/invite-not-found.html?form.invitationId=%s' %\
                            invitationId
        else: # Verification ID not specified
            uri = '/invite-no-id.html'
        assert uri
        assert type(uri) == str
        return self.request.RESPONSE.redirect(uri)

