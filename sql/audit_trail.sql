CREATE TABLE audit_event (
    id                  TEXT                        PRIMARY KEY,
    -- A unique identifier for the event, for potential linking of 
    --  the event to other tables.

    event_date          TIMESTAMP WITH TIME ZONE    NOT NULL,
    -- The date and time of the event.
    
    subsystem           TEXT                        NOT NULL,
    -- The subsystem related to the event (eg. email, profile, 
    -- group).
    
    event_code          TEXT                        NOT NULL,
    -- The event code (eg. notification, bounce, verification 
    -- request, verified). This is subsystem specific.

    user_id             TEXT                        DEFAULT NULL,
    -- The ID of the actor initiating the event. This may be null if 
    -- it is the system acting.
    
    instance_user_id    TEXT                        DEFAULT NULL,
    -- The ID of the user being *acted upon*. This may be null if 
    -- the ID cannot be identified (for example, a bounce for an 
    -- unknown email address).

    site_id             TEXT                        DEFAULT NULL,
    -- The site ID related to the event, if applicable.
    
    group_id            TEXT                        DEFAULT NULL,
    -- The group ID related to the event, if applicable.
    
    instance_datum      TEXT                        DEFAULT NULL,
    -- Data that may be required to assist in distinguishing this 
    -- specific instance of the event. For example, the email 
    -- address being sent a verification_request.

    supplementary_datum TEXT                        DEFAULT NULL
    -- Data related to the event, that may prove useful as part of 
    -- the log. For example, the actual bounce email in the event of 
    -- a bounce, or a message entered by the administrator 
    -- explaining a user ban.
);

