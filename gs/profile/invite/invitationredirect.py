# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
from invitation import Invitation

class GSInvitationResponseRedirect(GSRedirectBase):

    @property
    def ctx(self):
        return get_the_actual_instance_from_zope(self.context)
        
    def __call__(self):
        
        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            
            if (invitationId == 'example'):
                userInfo = createObject('groupserver.LoggedInUser',
                                        self.ctx)
                ref = self.request.get('HTTP_REFERER','')
                assert ref, 'This page only works if you follow the link '\
                    'from the invitation preview.'
                path = urlparse(ref)[2]
                groupId = path.split('/')[2]
                uri = '%s/intial_response.html?form.invitationId=example&form.groupId=%s' %\
                  (userInfo.url, groupId)
            else: # Not an example
                invitation = Invitation(self.ctx, invitationId)
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
                    uri = '%s/invitation-responded.html?form.invitationId=%s'%\
                            (invitation.siteInfo.url, invitationId)
                elif inviteExists and not(hadResponse) and not(invitationWithdrawn):
                    assert not invitation.userInfo.anonymous,\
                        'An invitation to an anonymous user. Let us '\
                        'hope you are on a development platform where '\
                        'such things happen, otherwise something has '\
                        'gone seriously wrong and you should contact '\
                        'support.'
                    # --=mpj17=-- Only ever log in when responding
                    login(self.ctx, invitation.userInfo.user)
                    if invitation.invite['initial_invite']:
                        # Go to the initial response page, so
                        #   the new user can set a password (and verify
                        #   his or her email address).
                        uri = '%s/%s/intial_response.html?form.invitationId=%s'%\
                                (invitation.siteInfo.url, 
                                invitation.userInfo.url, invitationId)
                    else:
                        # If the user is already a member of a group 
                        #   (any group on any site) then we should go to
                        #   the normal Response page.
                        uri = '%s/%s/invitations_respond.html' % \
                                (invitation.siteInfo.url, 
                                invitation.userInfo.url)
                elif inviteExists and invitationWithdrawn:
                    # The invitation has been withdrawn
                    uri = '%s/invitation-withdrawn.html?form.invitationId=%s'%\
                            (invitation.siteInfo.url, invitationId)
                else: # Invitation does not exist
                    uri = '%s/invite-not-found.html?form.invitationId=%s'%\
                            (invitation.siteInfo.url, invitationId)
        else: # Verification ID not specified
            uri = '/invite-no-id.html'
        assert uri
        assert type(uri) == str
        return self.request.RESPONSE.redirect(uri)

