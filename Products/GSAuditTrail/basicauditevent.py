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
import logging
log = logging.getLogger('Products.GSAuditTrail')
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from .interfaces import IAuditEvent


class BasicAuditEventFactory(object):
    implements(IFactory)

    title = 'Basic Audit Event Factory'
    description = 'Creates a basic GroupServer audit event'

    def __call__(self, context, *args):
        return BasicAuditEvent(context, args)

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class BasicAuditEvent(object):
    implements(IAuditEvent)

    def __init__(self, context, eventId, code='0', date=None, userInfo=None,
                    instanceUserInfo=None, siteInfo=None, groupInfo=None,
                    instanceDatum='', supplementaryDatum='', subsystem=''):
        if not context:
            raise ValueError('No context')
        self.context = context
        if not eventId:
            raise ValueError('No event ID')
        self.id = eventId

        self.code = code
        self.date = date
        self.userInfo = userInfo
        self.instanceUserInfo = instanceUserInfo
        self.siteInfo = siteInfo
        self.groupInfo = groupInfo
        self.instanceDatum = instanceDatum
        self.supplementaryDatum = supplementaryDatum
        self.subsystem = subsystem

    def __unicode__(self):
        r = '{0}: {1} ({2})'
        retval = r.format(self.subsystem, self.instanceDatum, self.date)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    def log(self):
        log.info(self)

    @property
    def xhtml(self):
        r = '<span class="audit-event-{0}">{1}: {2} '\
            '(<span class="date">{3}</span>)</span>'
        retval = r.format(self.code, self.subsystem, self.instanceDatum,
                            self.date)
        return retval
