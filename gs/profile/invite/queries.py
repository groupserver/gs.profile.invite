# coding=utf-8
import sqlalchemy as sa

class InvitationQuery(object):
    def __init__(self, context, da):
        self.context = context
        tableName = 'user_group_member_invitation'
        self.invitationTable = da.createTable(tableName)

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
        retval = {
            'invitation_id':    '',
            'user_id':          '',
            'inviting_user_id': '',
            'site_id':          '',
            'group_id':         '',
            'invitation_date':  '',
            'response_date':    '',
            'accepted':         ''}
        return retval

    def get_invitation(self, invitationId):
        it = self.invitationTable
        s = it.select()
        s.append_whereclause(it.c.invitation_id == invitationId)
        
        r = s.execute()
        if r.rowcount:
            x = r.fetchone()
            retval = self.marshal_invite(x)
        else:
            retval = self.get_blank_invite()
        return retval

    def get_only_invitation(self, userInfo):
        it = self.invitationTable
        s = it.select()
        s.append_whereclause(it.c.response_date == None)
        s.append_whereclause(it.c.user_id = userInfo.id )

        r = s.execute()
        assert r.rowcount < 2
        if r.rowcount:
            x = r.fetchone()
            retval = self.marshal_invite(x)
        else:
            retval = self.get_blank_invite()
        return retval

