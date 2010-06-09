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

class AuditEventFactory(object):
    implements(IFactory)

    title=u'User Profile Invitation Audit-Event Factory'
    description=u'Creates a GroupServer audit event for invitations'

    def __call__(self, context, event_id,  code, date,
        userInfo, instanceUserInfo,  siteInfo,  groupInfo,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if False:
          pass
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, 
              userInfo, instanceUserInfo, siteInfo, groupInfo, 
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)

class Auditor(object):
    def __init__(self, siteInfo, groupInfo, adminInfo, userInfo):
        self.siteInfo  = siteInfo
        self.groupInfo = groupInfo
        self.adminInfo = adminInfo
        self.userInfo  = userInfo
        
        da = userInfo.user.zsqlalchemy
        self.queries = AuditQuery(da)
      
        self.factory = AuditEventFactory()
        
    def info(self, code, instanceDatum = '', supplementaryDatum = ''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.adminInfo, self.userInfo,
            self.siteInfo, code, instanceDatum, supplementaryDatum)
          
        e = self.factory(self.userInfo.user, eventId,  code, d, 
                self.adminInfo,  self.userInfo, self.siteInfo, 
                self.groupInfo, instanceDatum, supplementaryDatum, 
                SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)

