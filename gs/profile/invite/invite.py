# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from zope.component import createObject
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSGroupMember.groupmembership import \
  user_member_of_group, invite_to_groups, user_admin_of_group
from Products.GSProfile import interfaces
from Products.GSProfile.utils import create_user_from_email, \
    enforce_schema
from Products.GSProfile.emailaddress import NewEmailAddress, \
    EmailAddressExists
from Products.GSGroup.changebasicprivacy import radio_widget
from utils import set_digest, send_add_user_notification

class InviteEditProfileForm(EditProfileForm):
    label = u'Invite a New Group Member'
    pageTemplateFileName = 'browser/templates/edit_profile_invite.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)

        siteInfo = self.siteInfo = \
          createObject('groupserver.SiteInfo', context)
        self.__groupsInfo = self.__groupInfo =  self.__formFields = None
        self.__config = self.__interface = self.__interfaceName = None
        self.__standardFieldIds = self.__standardFields = None
        self.__adminFields = self.__widgetNames = None

    def setUpWidgets(self, ignore_request=False):
        siteTz = self.siteInfo.get_property('tz', 'UTC')
        defaultTz = self.groupInfo.get_property('tz', siteTz)
        data = {'tz': defaultTz}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(interface, render_context=False)
            tz = self.__formFields['tz']
            tz.custom_widget = select_widget
            self.__formFields['biography'].custom_widget = wym_editor_widget
            self.__formFields['delivery'].custom_widget = radio_widget
        return self.formFields
    
    @form.action(label=u'Add', failure='handle_add_action_failure')
    def handle_add(self, action, data):
        self.actual_handle_add(action, data)

    # Non-Standard widgets below this point
    
    @property
    def config(self):
        if self.__config == None:
            site_root = self.context.site_root()
            assert hasattr(site_root, 'GlobalConfiguration')
            self.__config = site_root.GlobalConfiguration
        return self.__config
        
    @property
    def interface(self):
        if self.__interface == None:
            self.__interface = getattr(interfaces, self.interfaceName)
        return self.__interface
        
    @property
    def interfaceName(self):
        if self.__interfaceName == None:
            self.__interfaceName = '%sAdminJoinSingle' %\
              self.config.getProperty('profileInterface', 'IGSCoreProfile')
            assert hasattr(interfaces, self.__interfaceName), \
                'Interface "%s" not found.' % self.__interfaceName
        return self.__interfaceName
    
    @property
    def groupsInfo(self):
        if self.__groupsInfo == None:
            self.__groupsInfo = \
                createObject('groupserver.GroupsInfo', self.context)
        return self.__groupsInfo

    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            self.__groupInfo = \
                createObject('groupserver.GroupInfo', context)
        return self.__groupInfo
        
    @property
    def standardFieldIds(self):
        if self.__standardFieldIds == None:
            self.standardFieldIds = \
                [f[0] for f in getFieldsInOrder(self.interface)]
        return self.__standardFieldIds
        
    @property
    def widgetNames(self):
        if self.__widgetNames == None:
            self.__widgetNames = [w.name.split(w._prefix)[1]
                 for w in self.widgets]
        return self.__widgetNames
        
    @property
    def standardFields(self):
        if self.__standardFields == None:
            sfIds = self.standardFieldIds; wns = self.widgetNames
            self.__standardFields = [n for n in wns if n in sfIds]
        assert type(self.__standardFields) == list
        return self.__standardFields
        
    @property
    def adminFields(self):
        if self.__adminFields == None:
            sfIds = self.standardFieldIds; wns = self.widgetNames
            self.__adminFields = [n for n in wns if n not in sfIds]
            self.__adminFields.sort()
        assert type(self.__adminFields) == list
        return self.__adminFields
            
    def actual_handle_add(self, action, data):
        acl_users = self.context.acl_users
        email = data['email'].strip()
        
        # TODO: Audit
        
        # --=mpj17=-- As an EmailAddress field is used, we know that the
        #  email data is valid. However, the address could already on
        #  our system. So we use a NewEmailAddress field to check this :)
        emailChecker = NewEmailAddress(title=u'Email')
        emailChecker.context = self.context # --=mpj17=-- Legit?
        e = u'<code class="email">%s</code>' % email
        g = u'<a class="group" href="%s">%s</a>' % (self.groupInfo.url,
            self.groupInfo.name)
        try:
            emailChecker.validate(email)
        except EmailAddressExists, e:
            user = acl_users.get_userByEmail(email)
            assert user, 'User for address <%s> not found' % email
            userInfo = IGSUserInfo(user)
            u = u'<a href="%s" class="fn">%s</a>' % (userInfo.url, 
                userInfo.name)
            if user_member_of_group(user, self.groupInfo):
                self.status=u'''<li>The user with the email address %s 
&#8213; %s &#8213; is already a member of %s.</li>'''% (e, u, g)
                self.status = u'%s<li>No changes have been made.</li>' % \
                  self.status
            else:
                self.status=u'''<li>Inviting the existing user with the
email address %s &#8213; %s &#8213; to join %s.</li>'''% (e, u, g)
                invite_to_groups(userInfo, adminInfo, self.groupInfo)
        else:
            # Email address does not exist, but it is a legitimate address
            user = self.create_user(data)
            userInfo = IGSUserInfo(user)
            u = u'<a href="%s" class="fn">%s</a>' % (userInfo.url, 
                userInfo.name)
            self.status = u'''<li>The user %s has been created, and
given the email address %s.</li>''' % (u, e)
            #TODO Join the group on accept
            # join_group(user, self.groupInfo) 
            self.status = u'%s<li>An invitation to join %s has been'\
                'sent to %s.</li>' % (self.status, g, u)
        assert user, 'User not created or found'
        
    def handle_add_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    def create_user(self, data):
        email  = data['email'].strip()
        # TODO: Audit
                
        user = create_user_from_email(self.context, email)
        # Add profile attributes 
        enforce_schema(user, self.interface)
        changed = form.applyChanges(user, self.form_fields, data)
        set_digest(user, data)                
        # Send notification
        adminInfo = createObject('groupserver.LoggedInUser', self.context)
        send_add_user_notification(user, adminInfo.user, 
          self.groupInfo, data.get('message', ''))
        assert user
        return user

