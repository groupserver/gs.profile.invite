=====================
``gs.profile.invite``
=====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Responding to invitations to join a group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-09-15
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This part of the GroupServer user-profile code concerned with
sign up when an administrator invites someone to join a group. An
`existing user`_ or a `new user`_ can be invited.

Existing User
-------------

When an existing user is invited he or she is taken to a page
that shows the prospective member all the pending invitations.

New User
--------

A new user is sent an email that contains two links:

#. One to accept the invitation, and
#. Another to reject the invitation.

A redirector accepts or rejects the invitation, and takes the
user to the correct page.

Error Pages
-----------

Invitation Followed
~~~~~~~~~~~~~~~~~~~

This page is shown when a user, who has already accepted an
invitation, follows the invitation link again.

Invitation Rejected
~~~~~~~~~~~~~~~~~~~

This page is shown when a user, who has already rejected an
invitation, follows the invitation link again.

Note about Forms
================

All forms submit to themselves, as the view handles the data, as
it does with the XForms in GroupServer 0.9. We always post, as
almost all forms have a side-effect.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.profile.invite
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
