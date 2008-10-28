# coding=utf-8
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from interfaces import IAuditEvent

class BasicAuditEventFactory(object):
    implements(IFactory)

    title=u'Basic Audit Event Factory'
    description=u'Creates a basic GroupServer audit event'

    def __call__(self, context, *args):
        return BasicAuditEvent(context, args)
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)

class BasicAuditEvent(object):
    implements(IAuditEvent)
    def __init__(self,  context, id, code = '0', 
      date =None, userInfo = None, instanceUserInfo = None, 
      siteInfo = None, groupInfo = None, instanceDatum = '', 
      supplementaryDatum = '', subsystem = ''):
      
      assert context
      assert id
      self.context = context
      self.id = id
      
      self.code = code
      self.date = date
      self.userInfo = userInfo
      self.instanceUserInfo = instanceUserInfo
      self.siteInfo = siteInfo
      self.groupInfo = groupInfo
      self.instanceDatum = instanceDatum
      self.supplementaryDatum = supplementaryDatum
      self.subsystem = subsystem   

    def __str__(self):
        retval = '%s: %s (%s)' % (self.subsystem, self.instanceDatum,
                                  self.eventDate)
        return retval
        
    def log(self):
        log.info(self)
        
    @property
    def xhtml(self):
        retval = u'<span class="audit-event">%s: %s '\
          u'(<span class="date">%s</span>)</span>' % \
          (self.subsystem, self.instanceDatum, self.eventDate)
        return retval

