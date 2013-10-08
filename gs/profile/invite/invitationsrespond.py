# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy, cachedIn
from zope.component import createObject
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope
from gs.group.member.base.utils import user_member_of_group
from gs.group.member.join.interfaces import IGSJoiningUser
from gs.group.member.invite.base.queries import InvitationQuery
from gs.profile.base import ProfilePage
from gs.profile.notify.interfaces import IGSNotifyUser
from .invitation import Invitation
from .audit import Auditor, INVITE_RESPOND, INVITE_RESPOND_ACCEPT, \
    INVITE_RESPOND_DELCINE


class GSInviationsRespond(ProfilePage):
    '''The standard invitation response page.

    There are two pages used to respond to an invitation. The Initial
    Response page is used to set a password and accept the invitation,
    or decline the invitation. This page is used by existing members to
    accept and decline invitations.
    '''
    def __init__(self, profile, request):
        super(GSInviationsRespond, self).__init__(profile, request)

    @Lazy
    def ctx(self):
        return get_the_actual_instance_from_zope(self.context)

    @Lazy
    def groupsInfo(self):
        retval = createObject('groupserver.GroupsInfo', self.ctx)
        return retval

    @Lazy
    def invitationQuery(self):
        retval = InvitationQuery()
        return retval

    @cachedIn('_current_invitations')  # Note: @cachedIn, not @Lazy
    def currentInvitations(self):
        gci = self.invitationQuery.get_current_invitiations_for_site
        retval = [Invitation(self.ctx, i['invitation_id'])
                    for i in gci(self.siteInfo.id, self.userInfo.id)]
        assert type(retval) == list
        return retval

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

        if 'submitted' in form:
            groupIds = [k.split('-respond')[0] for k in form.keys()
              if '-respond' in k]
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
            assert 'error' in result, 'No "errror" in the result'
            assert type(result['error']) == bool
            assert 'message' in result, 'No "message" in the result'
            assert type(result['message']) == unicode

            # Invalidate the current invitations property, so it is recomputed.
            del self._current_invitations

        assert 'form' in result
        assert type(result['form']) == dict
        return result

    def accept_message(self, acceptedGroups):
        acceptedLinks = ['<a href="%s">%s</a>' % (g.relativeURL, g.name)
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
                    if (i.groupInfo.id in gids)]  # Skip groups already member

        auditor = Auditor(self.siteInfo, self.userInfo)

        for acceptedInvite in acceptedInvites:
            acceptedInvite.accept()
            auditor.info(INVITE_RESPOND, acceptedInvite.groupInfo,
                acceptedInvite.adminInfo, INVITE_RESPOND_ACCEPT)
            joiningUser = IGSJoiningUser(self.userInfo)
            # --=mpj17=-- Joining will notify the admin, by side effect.
            if not(user_member_of_group(self.userInfo, i.groupInfo)):
                joiningUser.join(acceptedInvite.groupInfo)
            # TODO: When anyone can invite anyone else to join more than
            #   the administrators will have to be informed.
            #   <https://projects.iopen.net/groupserver/ticket/436>
            #   The `decline_invitations` method does this currently.

    def decline_invitations(self, groupInfos):
        assert type(groupInfos) == list
        gids = [g.id for g in groupInfos]
        declinedInvites = [i for i in self.currentInvitations
                            if i.groupInfo.id in gids]

        auditor = Auditor(self.siteInfo, self.userInfo)

        for declinedInvite in declinedInvites:
            declinedInvite.decline()
            auditor.info(INVITE_RESPOND, declinedInvite.groupInfo,
                declinedInvite.adminInfo, INVITE_RESPOND_DELCINE)

            notifiedUser = IGSNotifyUser(declinedInvite.adminInfo)
            n_dict = {'userFn': self.userInfo.name,
                        'adminFn': declinedInvite.adminInfo.name,
                        'siteName': self.siteInfo.name,
                        'groupName': declinedInvite.groupInfo.name,
                        'groupURL': declinedInvite.groupInfo.url, }
            notifiedUser.send_notification('invite_join_group_declined',
                'default', n_dict)
