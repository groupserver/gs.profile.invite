# coding=utf-8
from Products.Five import BrowserView
from zope.component import createObject
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSGroupMember.utils import inform_ptn_coach_of_join
from Products.GSGroupMember.groupmembership import join_group
from queries import InvitationQuery
from invitation import Invitation

class GSInviationsRespond(BrowserView):
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.userInfo = IGSUserInfo(context)
        self.__groupsInfo = self.__currentInvitations = None
        self.__invitationQuery = None
    
    @property
    def groupsInfo(self):
        if self.__groupsInfo == None:
            self.__groupsInfo = createObject('groupserver.GroupsInfo', 
                self.context.aq_self)
        return self.__groupsInfo
    
    @property
    def invitationQuery(self):
        if self.__invitationQuery == None:
            da = self.context.zsqlalchemy
            assert da, 'No data-adaptor found'
            self.__invitationQuery = InvitationQuery(da)
        return self.__invitationQuery
        
    @property
    def currentInvitations(self):
        if self.__currentInvitations == None:
            gci = self.invitationQuery.get_current_invitiations_for_site
            self.__currentInvitations = \
                [Invitation(self.context.aq_self, i['invitation_id'])
                    for i in gci(self.siteInfo.id, self.userInfo.id)]
        assert type(self.__currentInvitations) == list
        return self.__currentInvitations

    def process_form(self):
        '''Process the forms in the page.
        
        This method uses the "submitted" pattern that is used for the
        XForms impementation on GroupServer. 
          * The method is called whenever the page is loaded by
            tal:define="result view/process_form".
          * The submitted form is checked for the hidden "submitted" field.
            This field is only returned if the user submitted the form,
            not when the page is loaded for the first time.
            - If the field is present, then the form is processed.
            - If the field is absent, then the method re  turns.
        
        RETURNS
            A "result" dictionary, that at-least contains the form that
            was submitted
        '''
        form = self.context.REQUEST.form
        result = {}
        result['form'] = form

        if form.has_key('submitted'):
            groupIds = [k.split('-respond')[0] for k in form.keys() 
              if  '-respond' in k]
            responses = [form['%s-respond' % k] for k in groupIds]          

            result['error'] = False            
            acceptedMessage = declinedMessage = u''

            accepted = [k.split('-accept')[0] for k in responses
              if '-accept' in k]
            if accepted:
                acceptedGroups = [createObject('groupserver.GroupInfo',
                  self.groupsInfo.groupsObj, g) for g in accepted]
                self.accept_invitations(acceptedGroups)
                acceptedMessage = self.accept_message(acceptedGroups)
                # TODO: tell someone
                
            declined = [k.split('-decline')[0] for k in responses 
                        if '-decline' in k]
            for d in declined:
                assert d not in accepted
            if declined:
                declinedGroups = [createObject('groupserver.GroupInfo',
                  self.groupsInfo.groupsObj, g) for g in declined]
                self.decline_invitations(declinedGroups)
                declinedMessage = self.decline_message(declinedGroups)

            result['message'] = u'%s\n%s' % \
                (acceptedMessage, declinedMessage)
            self.__currentInvitations = None
    
            assert result.has_key('error')
            assert type(result['error']) == bool
            assert result.has_key('message')
            assert type(result['message']) == unicode
        
        assert result.has_key('form')
        assert type(result['form']) == dict
        return result
        
    def accept_message(self, acceptedGroups):
        acceptedLinks = ['<a href="%s">%s</a>' % (g.url, g.name)
            for g in acceptedGroups]
        if len(acceptedLinks) > 1:
            c = u', '.join([g for g in acceptedLinks][:-1])
            a = u' and '.join((c, acceptedLinks[-1]))
            i = 'invitations'
            t = 'these groups'
        else:
            a = acceptedLinks[0]
            i = 'invitation'
            t = 'this group'
        retval = u'<p>You <strong>accepted</strong> the %s to join '\
            u'%s. You are now a member of %s.</p>' % (i, a, t)
        return retval
        
    def decline_message(self, declinedGroups):
        declinedLinks = ['<a href="%s">%s</a>' % (g.url, g.name)
            for g in declinedGroups]
        if len(declinedLinks) > 1:
            c = u', '.join([g for g in declinedLinks][:-1])
            a = u' and '.join((c, declinedLinks[-1]))
            i = 'invitations'
        else:
            a = declinedLinks[0]
            i = 'invitation'
        retval = u'<p>You <strong>declined</strong> the %s to '\
            u'join %s.</p>' % (i, a)
        return retval
        
    def accept_invitations(self, groupInfos):
        assert type(groupInfos) == list
        gids = [g.id for g in groupInfos]
        acceptedInvites = [i for i in self.currentInvitations 
                            if i.groupInfo.id in gids]
        for acceptedInvite in acceptedInvites:
            acceptedInvite.accept()
            join_group(self.context, acceptedInvite.groupInfo)
            self.notifiy_admin_accept(acceptedInvite.groupInfo)

    def decline_invitations(self, groupInfos):
        assert type(groupInfos) == list
        gids = [g.id for g in groupInfos]
        declinedInvites = [i for i in self.currentInvitations 
                            if i.groupInfo.id in gids]
        for declinedInvite in declinedInvites:
            declinedInvite.decline()
            self.notifiy_admin_decline(declinedInvite.groupInfo)

    def notifiy_admin_accept(self, groupInfo):
        self.notifiy_admin(groupInfo, 'invite_join_group_accepted')

        ptnCoachId = groupInfo.get_property('ptn_coach_id', '')
        if ptnCoachId:
            ptnCoachInfo = createObject('groupserver.UserFromId', 
                                        self.context, ptnCoachId)
            inform_ptn_coach_of_join(ptnCoachInfo, self.userInfo, groupInfo)
        
    def notifiy_admin_decline(self, groupInfo):
        self.notifiy_admin(groupInfo, 'invite_join_group_declined')

    def notifiy_admin(self, groupInfo, notificationId):
        invites = [i for i in self.currentInvitations
                   if i.groupInfo.id == groupInfo.id]

        n_dict = {
            'adminFn':   '',
            'userFn':    self.userInfo.name,
            'groupName': groupInfo.name,
            'groupURL':  groupInfo.url,
            'siteName':  self.siteInfo.name
        }

        seenAdmins = []
        for _invite in invites:
            adminInfo = createObject('groupserver.UserFromId', 
                                     self.context, 
                                     _invite.adminInfo.id)
            if adminInfo.id not in seenAdmins:
                seenAdmins.append(adminInfo.id)
                n_dict['adminFn'] = adminInfo.name
                adminInfo.user.send_notification(notificationId, 
                                                  'default', 
                                                  n_dict=n_dict)

