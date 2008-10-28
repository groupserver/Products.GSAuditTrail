# coding=utf-8
import sqlalchemy as sa
import pytz, datetime

from interfaces import IAuditEvent

import logging
log = logging.getLogger("GSAuditTrail") #@UndefinedVariable

class AuditQuery(object):
    def __init__(self, da):

        engine = da.engine
        metadata = sa.BoundMetaData(engine)
        self.auditEventTable = sa.Table(
          'audit_event', 
          metadata, 
          autoload=True)
    
    def store(self, event):
        if event.userInfo:
            euiid = event.userInfo.id
        else:
            euiid = ''

        if event.instanceUserInfo:
            eiuiid = event.instanceUserInfo.id
        else:
            eiuiid = ''

        if event.siteInfo:
            esiid = event.siteInfo.id
        else:
            esiid = ''

        if event.groupInfo:
            egiid = event.groupInfo.id
        else:
            egiid = ''

        i = self.auditEventTable.insert()
        i.execute(
          id = event.id,
          event_date = event.date,
          subsystem = event.subsystem,
          event_code = event.code,
          user_id = euiid,
          instance_user_id = eiuiid,
          site_id = esiid,
          group_id = egiid,
          instance_datum = event.instanceDatum,
          supplementary_datum = event.supplementaryDatum,
        )

    def get_user_events_on_site(self, user_id, site_id):
        aet = self.auditEvsentTable
        s = aet.select()
        s.append_whereclause(aet.c.user_id == user_id)
        s.append_whereclause(aet.c.site_id == site_id)
        s.order_by(sa.desc('date'))
        r = s.execute()

        retval = []
        if r.rowcount:
          retval = [{
            'id':                  x['id'],
            'date':                x['event_date'],
            'subsystem':           x['subsystem'],
            'event_code':          x['event_code'],
            'user_id':             x['user_id'],
            'instance_user_id':    x['instance_user_id'],
            'site_id':             x['site_id'],
            'group_id':            x['group_id'],
            'instance_datum':      x['instance_datum'],
            'supplementary_datum': x['supplementary_datum']} for x in r]
        assert type(retval) == list
        return retval

