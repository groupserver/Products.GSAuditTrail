# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from pytz import UTC
from zope.interface import Interface
from zope.schema import Datetime, Field, Text, TextLine


class IAuditEvent(Interface):
    '''An event that is recorded in the audit-trail system.

    Most of the fields map onto the fields in the audit-trail table,
    but an event can also render itself (as text and XHTML 1.0) and
    write itself to the Zope instance log.
    '''
    id = TextLine(  # FIXME: ID
        title='Event ID',
        description='The ID of the event',
        required=True)

    date = Datetime(
        title='Date',
        description='The date and time of the event.',
        required=True,
        default=datetime.now(UTC))

    subsystem = TextLine(
        title='Subsystem',
        description='The ID of the subsystem that generated the event',
        required=True)

    code = TextLine(
        title='Event Code',
        description='A code that specifies the type of event. This is '
                    'subsystem specific.',
        required=True)

    userInfo = Field(
        title='User Information',
        description='Information about the actor initiating the event. '
                    'This may be null if it is the system acting.',
        required=False)

    instanceUserInfo = Field(
        title='Instance User Information',
        description='The user being *acted upon*. This may be null if the '
                    'user cannot be identified.',
        required=False)

    siteInfo = Field(
        title='Site Information',
        description='Information about the site related to the event, if '
                    'applicable.',
        required=False)

    groupInfo = Field(
        title='Group Information',
        description='Information about the group related to the event, if '
                    'applicable.',
        required=False)

    instanceDatum = Text(
        title='Instance Datum',
        description='Data that may be required to assist in distinguishing '
                    'this specific instance of the event. For example, the '
                    'email address being sent a verification_request',
        required=False)

    supplementaryDatum = Text(
        title='Instance Datum',
        description='Data related to the event, that may prove useful as '
                    'part of the log. For example, the actual bounce email '
                    'in the event of a bounce, or a message entered by the '
                    'administrator explaining a user ban.',
        required=False)

    xhtml = TextLine(
        title='XHTML',
        description='A description of the event, in XHTML 1.0',
        required=True)

    def __str__():
        'A description of the event, in Unicode text'

    def log():
        """Log the event to the Zope instance log."""
