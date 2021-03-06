# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession


class AuditQuery(object):
    def __init__(self):
        self.auditEventTable = getTable('audit_event')

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
        session = getSession()
        params = {
          'id': event.id,
          'event_date': event.date,
          'subsystem': event.subsystem,
          'event_code': event.code,
          'user_id': euiid,
          'instance_user_id': eiuiid,
          'site_id': esiid,
          'group_id': egiid,
          'instance_datum': event.instanceDatum,
          'supplementary_datum': event.supplementaryDatum}
        session.execute(i, params=params)  # Here
        mark_changed(session)  # Really?

    def get_instance_user_events(self, user_id,
        site_id='', group_id='', limit=10, offset=0):
        """Get events that occurred to a particular user

        ARGUMENTS
            user_id:    The ID of the instance-user (required).
            site_id:    The ID of the site. Defaults to all ('').
            group_id:   The ID of the group. Defaults to all ('').
            limit:      The number of events to return. Default 10.
            offset:     The event-number to start searching from.
                        Defaults to 0 (most recent).

        RETURNS
            A list of dictionaries. The dictionaries can be fed to
            a Zope "createObject" call, to create the appropriate
            event.

        SIDE EFFECTS
          None.
        """
        aet = self.auditEventTable
        s = aet.select(limit=limit, offset=offset,
                       order_by=sa.desc('event_date'))
        s.append_whereclause(aet.c.instance_user_id == user_id)
        if site_id:
            s.append_whereclause(aet.c.site_id == site_id)
        if group_id:
            s.append_whereclause(aet.c.group_id == group_id)

        session = getSession()
        r = session.execute(s)
        retval = []
        if r.rowcount:
            retval = [{
                'event_id': x['id'],
                'date': x['event_date'],
                'subsystem': x['subsystem'],
                'code': x['event_code'],
                'user_id': x['user_id'],
                'instance_user_id': x['instance_user_id'],
                'site_id': x['site_id'],
                'group_id': x['group_id'],
                'instanceDatum': x['instance_datum'],
                'supplementaryDatum': x['supplementary_datum']} for x in r]
        assert type(retval) == list
        return retval
