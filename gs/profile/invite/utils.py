# coding=utf-8
import md5
from time import asctime
from Products.CustomUserFolder.interfaces import IGSUserInfo, ICustomUser
from Products.GSProfile.utils import userInfo_to_user, \
  verificationId_from_email
from queries import InvitationQuery
from Products.GSGroupMember.groupmembership import user_member_of_group,\
    userInfo_to_user, userInfo_to_user
from Products.XWFCore.XWFUtils import convert_int2b62

def set_digest(userInfo, data):
    delivery = 'delivery'
    email = 'email'
    digest = 'digest'
    web = 'web'
    assert data.has_key(delivery)
    assert data[delivery] in [email, digest, web]
    user = userInfo_to_user(userInfo)
    assert hasattr(user, 'set_enableDigestByKey')
    
    if data[delivery] == email:
        # --=mpj17=-- The default is one email per post
        pass
    elif data[delivery] == digest:
        user.set_enableDigestByKey(self.groupInfo.id)
    elif data[delivery] == web:
        user.set_disableDeliveryByKey(self.groupInfo.id)

def invite_id(siteId, groupId, userId, adminId, miscStr=''):
    istr = asctime() + siteId + groupId + userId + adminId + miscStr
    inum = long(md5.new(istr).hexdigest(), 16)
    retval = str(convert_int2b62(inum))
    assert retval
    assert type(retval) == str
    return retval

def send_add_user_notification(u, a, groupInfo, message=u''):
    """Send an Add User notification to a new user
    
    DESCRIPTION
      When a new user is added to the site, he or she needs to be informed
      of their new account. This function sends the appropriate 
      notification to the user.
      
    ARGUMENTS
      user        The instance of the user to add.
      admin       The instance of the administrator who is adding the user.
      groupInfo   Information about the group the user is being added to.
      message     An optional message to send to the user, in addition to
                  the standard message.
    RETURNS
      None.
      
    SIDE EFFECTS
      * Creates a verification-ID for the user's first (and only) email
        address and adds it to the email-address verification table.
      * Sends an "admin_create_new_user" message to the user, containing
        "message".
    """
    assert u
    user = userInfo_to_user(u)
    assert a
    admin = userInfo_to_user(a)
    assert admin.get_preferredEmailAddresses(), \
      'Admin has no preferred email addresses'
    #assert isinstance(admin, CustomUser)
    assert groupInfo
    assert (type(message) in (str, unicode)) or (message == None)
    
    siteInfo = groupInfo.siteInfo
    # As the user is a brand-new user, he or she only has one address.
    email = user.get_emailAddresses()[0]
    invitationId = verificationId_from_email(email)

    user.add_invitation(invitationId, admin.getId(),
      siteInfo.get_id(), groupInfo.get_id())
    user.add_emailAddressVerification(invitationId, email)
    
    
    # TODO: Fix this so the message is generated from a template.
    if message == None:
        message = ''
    
    n_dict = {}
    n_dict['verificationId'] = invitationId
    n_dict['userId'] = user.getId()
    n_dict['userFn'] = user.getProperty('fn','')
    n_dict['siteName'] = siteInfo.get_name()
    n_dict['groupName'] = groupInfo.get_name()
    n_dict['siteURL'] = siteInfo.get_url()
    n_dict['admin'] = {
      'name':    admin.getProperty('fn', ''),
      'address': admin.get_preferredEmailAddresses()[0],
      'message': message}
    
    user.send_notification(
      n_type='admin_create_new_user', 
      n_id='default',
      n_dict=n_dict, 
      email_only=[email])

def invite_to_groups(userInfo, invitingUserInfo, groups):
    '''Invite the user to join a group
    
    DESCRIPTION
      Invites an existing user to join a group.
      
    ARGUMENTS
      "user":       The CustomUser that is invited to join the group.
      "invitingUserInfo": The user that isi inviting the other to join the 
                          group.
      "groups":  The group (or groups) that the user is joined to.
      
    RETURNS
      None.
      
    SIDE EFFECTS
      An invitation is added to the database, and a notification is
      sent out to the user.
    '''
    assert IGSUserInfo.providedBy(userInfo), '%s is not a IGSUserInfo' %\
      userInfo
    assert IGSUserInfo.providedBy(invitingUserInfo),\
      '%s is not a IGSUserInfo' % userInfo

    # --=mpj17=-- Haskell an his polymorphism can get knotted
    if type(groups) == list:
        groupInfos = groups
    else:
        groupInfos = [groups]
    assert groupInfos != []
    
    siteInfo = groupInfos[0].siteInfo

    #--=mpj17=-- Arse to Zope. Really, arse to Zope and its randomly failing
    #            acquisition.
    da = siteInfo.siteObj.aq_parent.aq_parent.zsqlalchemy
    assert da, 'No data-adaptor found'
    invitationQuery = InvitationQuery(da)

    groupNames = []    
    for groupInfo in groupInfos:
        assert IGSGroupInfo.providedBy(groupInfo)
        inviteId = invite_id(siteInfo.id, groupInfo.id, 
                              userInfo.id, invitingUserInfo.id)
        invitationQuery.add_invitation(inviteId, siteInfo.id, groupInfo.id, 
            userInfo.id, invitingUserInfo.id)

        groupNames.append(groupInfo.name)

        if len(groupNames) > 1:
            c = u', '.join(groupNames[:-1])
            g = u' and '.join((c, groupNames[-1]))
        else:
            g = groupNames[0]
    
    # TODO: fix
    responseURL = '%s/r/group_invitation/%s' % (siteInfo.url, inviteId)
    n_dict={'userFn': userInfo.name,
            'invitingUserFn': invitingUserInfo.name,
            'siteName': siteInfo.name,
            'siteURL': siteInfo.url,
            'groupName': g,
            'responseURL': responseURL}
    userInfo.user.send_notification('invite_join_group', 'default', 
        n_dict=n_dict)

