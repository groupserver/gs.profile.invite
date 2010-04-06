Introduction
============

This part of the GroupServer usr-profile code concerned with sign up 
when an administrator invites someone to join a group. An `existing user`_
or a `new user`_ can be invited.

Existing User
-------------

When an existing user is invited he or she is taken to a page that
shows the prospective member all the pending invitations.

New User
--------


Note about Forms
================
All forms submit to themselves, as the view handles the data, as it does
with the XForms in GroupServer 0.9. We always post, as almost all forms
have a side-effect.

