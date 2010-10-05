# coding=utf-8
from pytz import UTC
from datetime import datetime
from md5 import new as new_md5
from zope.component import createObject
from Products.XWFCore.XWFUtils import convert_int2b62

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
    eNum = long(new_md5(e).hexdigest(), 16)
    eventId = str(convert_int2b62(eNum))
    assert type(eventId) == str
    return eventId

def marshal_data(context, data):
    assert context
    assert type(data) == dict
    retval = data
    
    uId = retval.pop('instance_user_id')
    retval['instanceUserInfo'] = \
      createObject('groupserver.UserFromId', context, uId)

    retval.pop('site_id')
    retval['siteInfo'] = \
      createObject('groupserver.SiteInfo', context)

    uId = retval.pop('user_id')
    retval['userInfo'] = \
      createObject('groupserver.UserFromId', context, uId)

    gId = retval.pop('group_id')
    retval['groupInfo'] = \
      createObject('groupserver.GroupInfo', context, gId)
    return retval

