# coding=utf-8
from zope.component import createObject
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSRedirect.view import GSRedirectBase
from gs.profile.invite.queries import InvitationQuery
from Products.GSProfile.utils import login

class GSInvitationResponseRedirect(GSRedirectBase):
    def __call__(self):

        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            user = self.get_userByGroupInvitationId(invitationId)
            
            if user:
                login(self.context, user)
                userInfo = IGSUserInfo(user)
            if (invitationId == 'example'):
                userInfo = createObject('groupserver.LoggedInUser',
                                        self.context)
            if (user or (invitationId == 'example')):
                # TODO: Audit
                # TODO: Figure out if it is the inital of subsequent 
                #  invite.
                #uri = '%s/invitations_respond.html' % userInfo.url
                uri = '%s/intial_response.html?form.invitationId=%s' %\
                  (userInfo.url, invitationId)
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
        if r['invitation_id']:
            site_root = self.context.site_root()
            acl_users = site_root.acl_users
            user = acl_users.getUser(r['user_id'])
        return user

