# coding=utf-8
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSRedirect.view import GSRedirectBase
from gs.profile.invite.queries import InvitationQuery
from Products.GSProfile.utils import login

import logging
log = logging.getLogger('GSGroupMember') #@UndefinedVariable

class GSInvitationResponseRedirect(GSRedirectBase):
    def __call__(self):

        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            user = self.get_userByGroupInvitationId(invitationId)
            
            if user:
                login(self.context, user)
                
                userInfo = IGSUserInfo(user)
                m = 'GSInvitationResponseRedirect: Going to the invitation '\
                  'response page for the ID %s for the user %s (%s).'  % \
                  (invitationId, userInfo.name, userInfo.id)
                log.info(m)

                uri = '%s/invitations_respond.html' % userInfo.url
            else: # Cannot find user
                uri = '/invite-user-not-found?id=%s' % invitationId
        else: # Verification ID not specified
            uri = '/invite-user-no-id'
        return self.request.RESPONSE.redirect(uri)

    def get_userByGroupInvitationId(self, invitationId):
        da = self.context.zsqlalchemy 
        assert da, 'No data-adaptor found'
        invitationQuery = InvitationQuery(da)
        r = invitationQuery.get_invitation(invitationId)
        user = None
        if r['inviation_id']:
            site_root = self.context.site_root()
            acl_users = site_root.acl_users
            user = acl_users.getUser(r['user_id'])
        return user

