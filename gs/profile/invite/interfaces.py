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
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.interface import Interface
from zope.schema import ASCIILine, Text, TextLine


class IGSSetPasswordAdminInvite(Interface):
    password1 = ASCIILine(title=u'Password',
        description=u'Your new password. For security, your password '
          u'should contain a mixture of letters and numbers, and '
          u'must be over four letters long.',
        required=True,
        min_length=4)

    invitationId = ASCIILine(title=u'Invitation Identifier',
      description=u'The identifier sent to you when you were invited to '
        u'join the group.',
      required=True)


class IGSResponseFields(Interface):
    invitationId = ASCIILine(title=u'Invitation Identifier',
        description=u'The identifier for the invitation to join the '
            u'group',
        required=True)

    groupId = ASCIILine(title=u'Group Identifier',
        description=u'The identifier for the group to join (for the) '
            u'preview.',
        required=False)

    password1 = TextLine(title=u'Password',
        description=u'Your new password. You will use it to log in to '
          u'this website. This will allow you to view your private '
          u'and secret groups, post from the '
          u'web, and change your profile.',
        required=False)


class IGSInvitationListContentProvider(IContentProvider):
    pageTemplateFileName = Text(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '
        u'render the invitation list.',
        required=False,
        default=u"browser/templates/invitationslist.pt")
