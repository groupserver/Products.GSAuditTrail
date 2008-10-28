# coding=utf-8
from zope.interface import Interface
from zope.schema import *

class IAuditEvent(Interface):
    '''An event that is recorded in the audit-trail system.
    
    Most of the fields map onto the fields in the audit-trail table,
    but an event can also render itself (as text and XHTML 1.0) and
    write itself to the Zope instance log.
    '''
    id = TextLine(title=u'Event ID',
      description=u'The ID of the event',
      required=True)

    date = Date(title=u'Date',
        description=u'The date and time of the event.',
        required=True)

    subsystem = TextLine(title=u'Subsystem',
      description=u'The ID of the subsystem that generated the '\
        u'event',
      required=True)

    code = TextLine(title=u'Event Code',
      description=u'A code that specifies the type of event. This '\
        u'is subsystem specific.',
      required=True)
      
    userInfo = Field(title=u'User Information',
      description=u'Information about the actor initiating the '\
        u'event. This may be null if it is the system acting.',
      required=False)

    instanceUserInfo = Field(title=u'Instance User Information',
      description=u' user being *acted upon*. '\
        u'This may be null if the user cannot be identified.',
      required=False)

    siteInfo = Field(title=u'Site Information',
      description=u'Information about the site related to the '\
        u'event, if applicable.',
      required=False)

    groupInfo = Field(title=u'Group Information',
      description=u'Information about the group related to the '\
        u'event, if applicable.',
      required=False)
      
    instanceDatum = Text(title=u'Instance Datum',
      description=u'Data that may be required to assist in '\
        u'distinguishing this specific instance of the event. For '\
        u'example, the email address being sent a '\
        u'verification_request',
      required=False)
      
    supplementaryDatum = Text(title=u'Instance Datum',
      description=u'Data related to the event, that may prove '\
        u'useful as part of the log. For example, the actual '\
        u'bounce email in the event of a bounce, or a message '\
        u'entered by the administrator explaining a user ban.',
      required=False)

    xhtml = TextLine(title=u'XHTML',
      description=u'A description of the event, in XHTML 1.0',
      required=True)
      
    def __str__():
      u'A description of the event, in Unicode text'

    def log():
        u"""Log the event to the Zope instance log."""

