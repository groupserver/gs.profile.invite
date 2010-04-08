# coding=utf-8
from zope.schema import *
from zope.interface.interface import Interface

class IGSSetPasswordAdminInvite(Interface):
    password1 = ASCIILine(title=u'Password',
        description=u'Your new password. For security, your password '\
          u'should contain a mixture of letters and numbers, and '\
          u'must be over four letters long.',
        required=True,
        min_length=4)

    invitationId = ASCIILine(title=u'Invitation Identifier',
      description=u'The identifier sent to you when you were invited to '\
        u'join the group.',
      required=True)

