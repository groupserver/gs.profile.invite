# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from operator import concat
from zope.component import createObject
from zope.formlib import form
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo, \
    userInfo_to_anchor
from Products.GSGroupMember.groupmembership import \
  user_member_of_group, user_admin_of_group
from Products.GSProfile.edit_profile import select_widget, wym_editor_widget
from Products.GSProfile.utils import create_user_from_email, \
    enforce_schema
from Products.GSProfile.emailaddress import NewEmailAddress, \
    EmailAddressExists
from Products.GSGroup.changebasicprivacy import radio_widget
from queries import InvitationQuery
from utils import set_digest, invite_to_groups, invite_id, \
    send_add_user_notification
from invitefields import InviteFields

class InviteEditProfileForm(PageForm):
    label = u'Invite a New Group Member'
    pageTemplateFileName = 'browser/templates/edit_profile_invite.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)

        siteInfo = self.siteInfo = \
          createObject('groupserver.SiteInfo', context)
        self.__groupInfo = self.__formFields =  self.__config = None
        self.__adminInfo = self.__invitationQuery = None
        self.inviteFields = InviteFields(context)

    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(self.inviteFields.adminInterface, 
                render_context=False)
            tz = self.__formFields['tz']
            tz.custom_widget = select_widget
            self.__formFields['biography'].custom_widget = wym_editor_widget
            self.__formFields['delivery'].custom_widget = radio_widget
        return self.__formFields
        
    def setUpWidgets(self, ignore_request=False):
        siteTz = self.siteInfo.get_property('tz', 'UTC')
        defaultTz = self.groupInfo.get_property('tz', siteTz)
        data = {'tz': defaultTz}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)
        
    @form.action(label=u'Invite', failure='handle_invite_action_failure')
    def handle_invite(self, action, data):
        self.actual_handle_add(action, data)
        
    def handle_invite_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    # Non-Standard methods below this point
    @property
    def groupInfo(self):
        if self.__groupInfo == None:
            self.__groupInfo = \
                createObject('groupserver.GroupInfo', self.context)
        return self.__groupInfo
        
    @property
    def adminInfo(self):
        if self.__adminInfo == None:
            self.__adminInfo = createObject('groupserver.LoggedInUser', 
                self.context)
        return self.__adminInfo
    
    @property
    def invitationQuery(self):
        if self.__invitationQuery == None:
            da = self.context.zsqlalchemy
            self.__invitationQuery = InvitationQuery(da)
        return self.__invitationQuery
        
    def actual_handle_add(self, action, data):
        acl_users = self.context.acl_users
        email = data['email'].strip()
        
        # TODO: Audit
        
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
            u = userInfo_to_anchor(userInfo)
            
            if user_member_of_group(user, self.groupInfo):
                self.status=u'''<li>The person with the email address %s 
&#8213; %s &#8213; is already a member of %s.</li>'''% (e, u, g)
                self.status = u'%s<li>No changes have been made.</li>' % \
                  self.status
            else:
                self.status=u'''<li>Inviting the existing person with the
email address %s &#8213; %s &#8213; to join %s.</li>'''% (e, u, g)
                #TODO check: invite_to_groups(userInfo, adminInfo, self.groupInfo)
        else:
            # Email address does not exist, but it is a legitimate address
            user = create_user_from_email(self.context, email)
            userInfo = IGSUserInfo(user)
            self.add_profile_attributes(userInfo, data)
            inviteId = self.create_invitation(userInfo, data)
            self.send_notification(userInfo, inviteId)
            
            u = userInfo_to_anchor(userInfo)
            self.status = u'''<li>A profile for %s has been created, and
given the email address %s.</li>''' % (u, e)
            self.status = u'%s<li>An invitation to join %s has been'\
                'sent to %s.</li>' % (self.status, g, u)
        assert user, 'User not created or found'
        assert self.status
        
    def handle_add_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

    def add_profile_attributes(self, userInfo, data)
        enforce_schema(userInfo.user, self.inviteFields.profileInterface)
        changed = form.applyChanges(userInfo,user, self.form_fields, data)
        set_digest(userInfo, data)

    def create_invitation(self, userInfo, data):
        miscStr = reduce(concat, [str(i) for i in data.values()], '')
        inviteId = inviteId(self.siteInfo.id, self.groupInfo.id, 
            self.adminInfo.id, miscStr)
        self.invitationQuery.add_invitation(inviteId, self.siteInfo.id,
            self.groupInfo.id, self.userInfo.id, self.adminInfo.id, True)
        return inviteId
        
    def send_notificataion(self, userInfo, inviteId):
        # TODO: Fix
        send_add_user_notification(userInfo.user, self.adminInfo.user, self.groupInfo, 
                                    data.get('message', ''))

