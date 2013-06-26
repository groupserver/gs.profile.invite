# -*- coding: utf-8 -*-
from urlparse import urlparse
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
from gs.profile.email.base.emailuser import EmailUser
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
                ref = self.request.get('HTTP_REFERER', '')
                assert ref, 'This page only works if you follow the link '\
                    'from the invitation preview.'
                path = urlparse(ref)[2]
                groupId = path.split('/')[2]
                uri = '%s/initial_response.html?form.invitationId=example&'\
                        'form.groupId=%s' % (userInfo.url, groupId)
            else:  # Not an example
                invitation = Invitation(self.ctx, invitationId)
                try:
                    hadResponse = \
                        invitation.invite['response_date'] is not None
                    invitationWithdrawn = \
                        invitation.invite['withdrawn_date'] is not None
                except KeyError:
                    hadResponse = inviteExists = invitationWithdrawn = False
                else:
                    inviteExists = True

                if inviteExists and hadResponse:
                    uri = '/invitation-responded.html?form.invitationId=%s' %\
                            (invitationId)
                elif (inviteExists and not(hadResponse)
                        and not(invitationWithdrawn)):
                    assert not invitation.userInfo.anonymous,\
                        'An invitation to an anonymous user. Let us '\
                        'hope you are on a development platform where '\
                        'such things happen, otherwise something has '\
                        'gone seriously wrong and you should contact '\
                        'support.'
                    # --=mpj17=-- Only ever log in when responding
                    login(self.ctx, invitation.userInfo.user)
                    # I used to use the "initial_invite" column, but now
                    #   it is unused.
                    emailUser = EmailUser(self.ctx, invitation.userInfo)
                    initial = bool(emailUser.get_verified_addresses())
                    if not(initial):
                        # Go to the initial response page, so
                        #   the new user can set a password (and verify
                        #   his or her email address).
                        uri = '%s/initial_response.html?form.invitationId=%s' %\
                            (invitation.userInfo.url, invitationId)
                    else:
                        # If the user is already a member of a group
                        #   (any group on any site) then we should go to
                        #   the normal Response page.
                        uri = '%s/invitations_respond.html' % \
                            (invitation.userInfo.url)
                elif inviteExists and invitationWithdrawn:
                    # The invitation has been withdrawn
                    uri = '/invitation-withdrawn.html?form.invitationId=%s' %\
                            (invitationId)
                else:  # Invitation does not exist
                    uri = '/invite-not-found.html?form.invitationId=%s' %\
                            (invitationId)
        else:  # Verification ID not specified
            uri = '/invite-no-id.html'
        assert uri
        assert type(uri) == str
        return self.request.RESPONSE.redirect(uri)
