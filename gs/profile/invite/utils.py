# coding=utf-8
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


