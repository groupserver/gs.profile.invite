# coding=utf-8
from urlparse import urlparse
from zope.component import createObject
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSRedirect.view import GSRedirectBase
from gs.profile.invite.queries import InvitationQuery
from Products.GSProfile.utils import login

class GSInvitationResponseRedirect(GSRedirectBase):
    def __call__(self):
        # TODO: Audit
        if len(self.traverse_subpath) == 1:
            invitationId = self.traverse_subpath[0]
            user = self.get_userByGroupInvitationId(invitationId)
            
            if user:
                login(self.context, user)
                userInfo = IGSUserInfo(user)
                # TODO: Figure out if it is the inital of subsequent 
                #  invite.
                uri = '%s/intial_response.html?form.invitationId=%s' %\
                  (userInfo.url, invitationId)
            elif (invitationId == 'example'):
                userInfo = createObject('groupserver.LoggedInUser',
                                        self.context)
                ref = self.request.get('HTTP_REFERER','')
                assert ref, 'This page only works if you follow the link '\
                    'from the invitation preview.'
                path = urlparse(ref)[2]
                groupId = path.split('/')[2]
                uri = '%s/intial_response.html?form.invitationId=example&form.groupId=%s' %\
                  (userInfo.url, groupId)
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

