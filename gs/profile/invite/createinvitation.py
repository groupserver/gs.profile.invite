# coding=utf-8
'''The form that allows an admin to invite a new person to join a group.'''
from textwrap import wrap
from operator import concat
from email.Message import Message
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from zope.contentprovider.tales import addTALNamespaceData
from Products.XWFCore.XWFUtils import get_support_email
from invitationmessagecontentprovider import InvitationMessageContentProvider

utf8 = 'utf-8'
def create_invitation(view, userInfo, inviteId, data):
    cp = InvitationMessageContentProvider(view.context, view.request, view)
    view.vars = {}
    addTALNamespaceData(cp, view.context)
    
    cp.preview = False

    toAddr = u'"%s" <%s>' % (userInfo.name, data['toAddr'].strip())
    cp.toAddr = str(Header(toAddr, utf8))
    
    fromAddr = u'"%s" <%s>' % (view.adminInfo.name, data['fromAddr'].strip())
    cp.fromAddr = str(Header(fromAddr, utf8))
    
    subject = str(Header(data['subject'], utf8))
    cp.subject = subject
    
    cp.body = data['message']
    cp.invitationId = inviteId

    cp.text = True
    cp.update()
    t = cp.render().strip()
    text = MIMEText(t, 'plain', utf8)
    
    cp.text = False
    cp.body = data['message'].strip().replace('\n', '<br/>')
    h = cp.render()
    html = MIMEText(h, 'html', utf8)
    
    container = MIMEMultipart('alternative')
    container.attach(text)
    container.attach(html)

    msg = Message()
    msg['Subject'] = cp.subject
    msg['From'] = cp.fromAddr
    msg['To'] = cp.toAddr
    e = get_support_email(view.context, view.siteInfo.id)
    replyToAddr = u'"%s Support" <%s>' % (view.siteInfo.name, e)
    msg['Reply-to'] = str(Header(replyToAddr, utf8))
    msg.set_payload(container.as_string())
    print msg.as_string()

