# coding=utf-8
import sqlalchemy as sa

class InvitationQuery(object):
    def __init__(self, context, da):
        self.context = context
        tableName = 'user_group_member_invitation'
        self.invitationTable = da.createTable(tableName)

    def get_invitation(self, invitationId):
        it = self.invitationTable
        s = it.select()
        s.append_whereclause(invitation_id == invitationId)
        
        r = s.execute()
        
        if r.rowcount:
            x = r.fetchone()
            retval = {
                'invitation_id':    x['invitation_id'],
                'user_id':          x['user_id'],
                'inviting_user_id': x['inviting_user_id'],
                'site_id':          x['site_id'],
                'group_id':         x['group_id'],
                'invitation_date':  x['invitation_date'],
                'response_date':    x['response_date'],
                'accepted':         x['accepted']}
        else:
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

