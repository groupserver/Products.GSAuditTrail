=========================
``Products.GSAuditTrail``
=========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The audit-trail for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-02-16
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

The *audit trail* system in GroupServer is a variant of a
structured log file, kept in an SQL database table_. A `base
class`_ provides a *very* *basic* system for mapping
audit-objects to rows in a relational database

Table
=====

The ``audit_event`` table defines the information about each
event.

``id``:
  A unique identifier for the event, for potential linking of the
  event to other tables.

``event_date``:
  The date and time of the event.
    
``subsystem``:
  The subsystem related to the event (eg. email, profile, group).
    
``event_code``:
  The event code (eg. notification, bounce, verification request,
  verified). This is subsystem specific.

``user_id``:
  The ID of the actor initiating the event. This may be null if
  it is the system acting.
    
``instance_user``:
  The ID of the user being *acted upon*. This may be null if the
  ID cannot be identified (for example, a bounce for an unknown
  email address).

``site_id``:
    -- The site ID related to the event, if applicable.
    
``group_id``:
  The group ID related to the event, if applicable.
    
``instance_datum``:
  Data that may be required to assist in distinguishing this
  specific instance of the event. For example, the email address
  being sent a verification_request.

``supplementary_datum``:
  Data related to the event, that may prove useful as part of the
  log. For example, the actual bounce email in the event of a
  bounce, or a message entered by the administrator explaining a
  user ban.


Base class
==========

The ``Products.GSAuditTrail.BasicAuditEvent`` provides a basic
class that more specific audit-event class.

Resources
=========

- Code repository: https://github.com/groupserver/Products.GSAuditTrail
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  SQL GSAuditTrail Organization
