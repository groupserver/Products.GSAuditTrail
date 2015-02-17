# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from time import sleep
from unittest import TestCase
from Products.GSAuditTrail.utils import event_id_from_data


class Info(object):
    def __init__(self, infoId, name):
        self.id = infoId
        self.name = name


class TestEventId(TestCase):
    '''Test the event_id_from_data generator, which is prone to Unicode
issues'''

    def setUp(self):
        self.userInfo = Info('user', 'User Info')
        self.instanceUserInfo = Info('instance-user', 'Instance User Info')
        self.siteInfo = Info('site', 'Site Info')

    def test_event_id(self):
        'Basic test, with just Unicode'
        r = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c', None,
            None)
        self.assertIsNotNone(r)
        self.assertGreater(len(r), 1)

    def test_event_id_time(self):
        'Check that time changes the ID'
        r0 = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c', None,
            None)
        sleep(1)
        r1 = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c', None,
            None)

        self.assertNotEqual(r0, r1, 'Time has no effect on the identifier')

    def test_event_id_data(self):
        'Unicode data'
        r = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c', 'foo',
            'bar')
        self.assertIsNotNone(r)
        self.assertGreater(len(r), 1)

    def test_event_id_data_change(self):
        'Test that changing data changes the ID'
        r0 = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c', 'foo',
            'bar')
        r1 = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, 'c',
            'wibble', 'blarg')
        self.assertNotEqual(r0, r1)

    def test_ascii(self):
        'Test that ascii data does not thow the creation of IDs'
        self.userInfo.id = b'user'
        self.userInfo.name = b'User name'
        self.instanceUserInfo.id = b'instance user'
        self.instanceUserInfo.name = b'Instance User Info'
        self.siteInfo.id = b'site'
        self.siteInfo.name = b'Site Info'
        r = event_id_from_data(
            self.userInfo, self.instanceUserInfo, self.siteInfo, b'c',
            b'foo', b'bar')
        self.assertIsNotNone(r)
        self.assertGreater(len(r), 1)

    def test_utf8(self):
        'Test that UTF-8 data does not throw the creation of IDs'
        self.userInfo.id = '\u2019user\2020'.encode('utf-8')
        self.userInfo.name = 'User\u2014name'.encode('utf-8')
        self.instanceUserInfo.id = 'instance user\u293c'.encode('utf-8')
        self.instanceUserInfo.name = 'Instance User '\
                                     'Info\203d'.encode('utf-8')
        self.siteInfo.id = 'site\u2047'
        self.siteInfo.name = 'Site Info\2048'
