# coding=utf-8
import pytz
from datetime import  datetime
import sqlalchemy as sa

class InvitationQuery(object):
    def __init__(self, da):
        self.userInvitationTable = da.createTable('user_group_member_invitation')

    def marshal_invite(self, x):
        retval = {
            'invitation_id':    x['invitation_id'],
            'user_id':          x['user_id'],
            'inviting_user_id': x['inviting_user_id'],
            'site_id':          x['site_id'],
            'group_id':         x['group_id'],
            'invitation_date':  x['invitation_date'],
            'response_date':    x['response_date'],
            'accepted':         x['accepted']}
        return retval
        
    def get_blank_invite(self):
        retval = {'invitation_id':'', 'user_id':'', 
            'inviting_user_id':'', 'site_id':'', 'group_id':'', 
            'invitation_date':'', 'response_date':'', 'accepted':''}
        return retval

    def get_invitation(self, invitationId, current=True):
        uit = self.userInvitationTable
        s = uit.select()
        s.append_whereclause(uit.c.invitation_id == invitationId)
        if current:
            s.append_whereclause(uit.c.response_date == None)
        r = s.execute()

        if r.rowcount:
            x = r.fetchone()
            retval = self.marshal_invite(x)
        else:
            retval = self.get_blank_invite()
        return retval
            
    def get_current_invitiations_for_site(self, siteId, userId):
        assert siteId
        assert userId
        uit = self.userInvitationTable
        cols = [uit.c.invitation_id, uit.c.user_id, 
            uit.c.inviting_user_id, uit.c.site_id, uit.c.group_id,
            uit.c.invitation_date,
            uit.c.response_date, uit.c.accepted] #@UndefinedVariable
        s = sa.select(cols)
        s.append_whereclause(uit.c.site_id  == siteId)
        s.append_whereclause(uit.c.user_id  == userId)
        s.append_whereclause(uit.c.response_date == None)
        #s.order_by(sa.desc('date'))
        #s.group_by(uit.c.site_id, uit.c.group_id, uit.c.user_id, 
        #    uit.c.inviting_user_id)
        r = s.execute()

        retval = []
        if r.rowcount:
            retval = [self.marshal_invite(x) for x in r]
        assert type(retval) == list
        return retval

    def get_past_invitiations_for_site(self, siteId, userId):
        assert siteId
        assert userId
        uit = self.userInvitationTable
        cols = [uit.c.site_id, uit.c.group_id, uit.c.user_id, 
                uit.c.inviting_user_id, uit.c.invitation_date,
                uit.c.response_date, uit.c.accepted]
        s = sa.select(cols, distinct=True)
        s.append_whereclause(uit.c.site_id  == siteId)
        s.append_whereclause(uit.c.user_id  == userId)
        s.append_whereclause(uit.c.response_date != None)
        s.order_by(sa.desc(uit.c.invitation_date))

        r = s.execute()

        retval = []
        if r.rowcount:
            retval = [self.marshal_invite(x) for x in r]
        assert type(retval) == list
        return retval

    def get_invitations_sent_by_user(self, siteId, invitingUserId):
        assert siteId
        assert invitingUserId
        uit = self.userInvitationTable
        cols = [uit.c.site_id, uit.c.group_id, uit.c.user_id, 
                uit.c.invitation_date, uit.c.response_date, uit.c.accepted]
        s = sa.select(cols, distinct=True)
        s.append_whereclause(uit.c.site_id  == siteId)
        s.append_whereclause(uit.c.inviting_user_id  == invitingUserId)
        s.order_by(sa.desc(uit.c.invitation_date))

        r = s.execute()

        retval = []
        if r.rowcount:
            retval = [self.marshal_invite(x) for x in r]
        assert type(retval) == list
        return retval

    def get_only_invitation(self, userInfo):
        it = self.userInvitationTable
        s = it.select()
        s.append_whereclause(it.c.response_date == None)
        s.append_whereclause(it.c.user_id == userInfo.id )

        r = s.execute()
        assert r.rowcount < 2
        if r.rowcount:
            x = r.fetchone()
            retval = self.marshal_invite(x)
        else:
            retval = self.get_blank_invite()
        return retval

    def accept_invitation(self, siteId, groupId, userId):
        self.alter_invitation(siteId, groupId, userId, True)
        
    def decline_invitation(self, siteId, groupId, userId):
        self.alter_invitation(siteId, groupId, userId, False)
        
    def alter_invitation(self, siteId, groupId, userId, status):
        assert siteId
        assert groupId
        assert userId
        assert type(status) == bool

        d = datetime.utcnow().replace(tzinfo=pytz.utc)        
        uit = self.userInvitationTable
        c = sa.and_(
          uit.c.site_id  == siteId, 
          uit.c.group_id == groupId,
          uit.c.user_id  == userId)
        v = {uit.c.response_date: d, uit.c.accepted: status}
        u = uit.update(c, values=v)
        u.execute()        

