# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from zope.component import createObject
from zope.formlib import form
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSGroup.changebasicprivacy import radio_widget
from gs.profile.notify.interfaces import IGSNotifyUser
from gs.profile.notify.adressee import Addressee, SupportAddressee
from queries import InvitationQuery
from utils import send_add_user_notification
from audit import Auditor, INVITE_RESPOND

class InviteEditProfileForm(PageForm):
    label = u'Invite a New Group Member'
    pageTemplateFileName = 'browser/templates/initialresponse.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)

        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.__formFields = self.__invitationQuery = None
        self.__adminInfo = self.__userInfo = self.__groupInfo = None
        self.__groupPrivacy = self.__groupStats = None
        
    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(IGSResponseFields, 
                                            render_context=False)
            response = self.__formFields['response']
            response.custom_widget = radio_widget
        return self.__formFields

    @form.action(label=u'Respond', failure='handle_respond_action_failure')
    def handle_invite(self, action, data):
        self.actual_handle_respond(action, data)
        
    def handle_respond_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
            
    # Non-Standard methods below this point
    @property
    def adminInfo(self):
        pass

    @property
    def userInfo(self):
        pass

    @property
    def groupInfo(self):
        pass

    @property
    def groupPrivacy(self):
        pass

    @property
    def groupStats(self):
        pass

    @property
    def invitationQuery(self):
        if self.__invitationQuery == None:
            da = self.context.zsqlalchemy
            self.__invitationQuery = InvitationQuery(da)
        return self.__invitationQuery

