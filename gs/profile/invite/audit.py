# coding=utf-8
from pytz import UTC
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape
from base64 import b64decode
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
  AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date

SUBSYSTEM = 'gs.profile.invite'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN         = '0'
INVITE_RESPOND  = '3'

INVITE_RESPOND_ACCEPT  = 'accepted'
INVITE_RESPOND_DELCINE = 'declined'

class AuditEventFactory(object):
    implements(IFactory)

    title=u'User Profile Invitation Audit-Event Factory'
    description=u'Creates a GroupServer audit event for invitations'

    def __call__(self, context, event_id,  code, date,
        userInfo, instanceUserInfo,  siteInfo,  groupInfo,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == INVITE_RESPOND:
          event = RespondEvent(context, event_id, date, userInfo,
          instanceUserInfo, siteInfo, groupInfo, instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, 
              userInfo, instanceUserInfo, siteInfo, groupInfo, 
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)

class RespondEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person responding to an 
    invitation.
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, adminInfo, instanceUserInfo, 
                  siteInfo, groupInfo, response):
        """ Create a respnd-event
        """
        BasicAuditEvent.__init__(self, context, id,  INVITE_RESPOND, d, 
            adminInfo, instanceUserInfo, siteInfo, groupInfo, response, 
            None, SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) has %s the invitation from %s (%s) to '\
            u'join %s (%s) on %s (%s).' %\
           (self.instanceUserInfo.name, self.instanceUserInfo.id,
            self.instanceDatum,
            self.userInfo.name,         self.userInfo.id,
            self.groupInfo.name,        self.groupInfo.id,
            self.siteInfo.name,         self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-profile-invite-%s' %\
          self.code
        retval = u'<span class="%s">%s the invitation to join %s</span>'%\
          (cssClass, self.instanceDatum.title(), self.groupInfo.name)
        
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class Auditor(object):
    def __init__(self, siteInfo, userInfo):
        self.siteInfo = siteInfo
        self.userInfo  = userInfo
        
        da = userInfo.user.zsqlalchemy
        self.queries = AuditQuery(da)
      
        self.factory = AuditEventFactory()
        
    def info(self, code, groupInfo, adminInfo, instanceDatum = '', supplementaryDatum = ''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(adminInfo, self.userInfo,
            self.siteInfo, code, instanceDatum, supplementaryDatum)
          
        e = self.factory(self.userInfo.user, eventId,  code, d, 
                adminInfo,  self.userInfo, self.siteInfo, groupInfo, 
                instanceDatum, supplementaryDatum, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)

