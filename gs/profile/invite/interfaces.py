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

class IGSInvitationMessage(Interface):
    text = Bool(title=u'Text',
        description=u'Display the invitation as pure text, rather than '\
            u'a HTML pre-element. Call it command  coupling if you '\
            u'want, it is how the code works.',
        required=False,
        default=False)

    toAddr = ASCIILine(title=u'To', 
        description=u'The email address of the person receiving the '\
            u'invitation.',
        required=True)

    fromAddr = ASCIILine(title=u'To', 
        description=u'The email address of the person sending the '\
            u'invitation.',
        required=True)

    subject = TextLine(title=u'Subject',
        description=u'The subject-line of the invitation.',
        required=True)

    body = Text(title=u'Body',
        description=u'The body of the invitation.',
        required=True)

class IGSInvitationMessageContentProvider(IGSInvitationMessage):
    pageTemplateFileName = Text(title=u"Page Template File Name",
      description=u'The name of the ZPT file that is used to render the '\
        u'status message.',
      required=False,
      default=u"browser/templates/invitationmessagecontentprovider.pt")

