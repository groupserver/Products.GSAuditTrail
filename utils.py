# coding=utf-8
from pytz import UTC
from datetime import datetime
from md5 import new as new_md5
from Products.XWFCore.XWFUtils import convert_int2b62

def event_id_from_data(userInfo, instanceUserInfo, siteInfo, code,
                       instanceDatum, supplementaryDatum):
    e = '%s-%s %s-%s %s-%s %s %s %s %s' % \
      (userInfo.name, userInfo.id, instanceUserInfo.name, 
       instanceUserInfo.id, siteInfo.name, siteInfo.id, 
       datetime.now(UTC), code, instanceDatum, supplementaryDatum)
    eNum = long(new_md5(e).hexdigest(), 16)
    eventId = str(convert_int2b62(eNum))
    assert type(eventId) == str
    return eventId

