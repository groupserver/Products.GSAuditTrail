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
from datetime import datetime
from pytz import UTC
from zope.component import createObject
from gs.core import to_id

ascii = 'ascii'
ignore = 'ignore'


def event_id_from_data(userInfo, instanceUserInfo, siteInfo, code,
                       instanceDatum, supplementaryDatum):
    e = '%s-%s %s-%s %s-%s %s %s %s %s' % \
      (userInfo.name.encode(ascii, ignore), userInfo.id,
       instanceUserInfo.name.encode(ascii, ignore), instanceUserInfo.id,
       siteInfo.name.encode(ascii, ignore), siteInfo.id,
       datetime.now(UTC), code, instanceDatum.encode(ascii, ignore),
       supplementaryDatum.encode(ascii, ignore))
    retval = to_id(e)
    return retval


def marshal_data(context, data, siteInfo=None, groupInfo=None):
    assert context
    assert type(data) == dict
    retval = data

    uId = retval.pop('instance_user_id')
    retval['instanceUserInfo'] = \
      createObject('groupserver.UserFromId', context, uId)

    retval.pop('site_id')
    if not siteInfo:
        siteInfo = \
          createObject('groupserver.SiteInfo', context)
    retval['siteInfo'] = siteInfo

    uId = retval.pop('user_id')
    retval['userInfo'] = \
      createObject('groupserver.UserFromId', context, uId)

    gId = retval.pop('group_id')
    if not(groupInfo) and gId:
        groupInfo = \
          createObject('groupserver.GroupInfo', siteInfo.siteObj, gId)
    retval['groupInfo'] = groupInfo
    return retval
