# coding=utf-8
from zope.component import createObject
from zope.formlib import form
from Products.Five.formlib.formbase import PageForm

class InvitationMessage(PageForm):
    label = u'Invite a New Group Member'
    pageTemplateFileName = 'browser/templates/invitation_message.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    self.form_fields = form.Fields(IGSInvitationMessage, render_context=False)
    
    def __init__(self, context, request):
        PageForm.__init__(self, context, request)

        siteInfo = self.siteInfo = \
          createObject('groupserver.SiteInfo', context)
        self.__groupInfo = self.__formFields =  self.__config = None
        self.__adminInfo = self.__invitationQuery = None
        self.inviteFields = InviteFields(context)
        
    @form.action(label=u'Invite', failure='handle_invite_action_failure')
    def handle_invite(self, action, data):
        raise NotImplemented
        
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

