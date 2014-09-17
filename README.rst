Introduction
============

This part of the GroupServer user-profile code concerned with sign up 
when an administrator invites someone to join a group. An `existing user`_
or a `new user`_ can be invited.

Existing User
-------------

When an existing user is invited he or she is taken to a page that
shows the prospective member all the pending invitations.

New User
--------

A new user is sent an email that contains two links:

#. One to accept the invitation, and
#. Another to reject the invitation.

A redirector accepts or rejects the invitation, and takes the user to
the correct page.

Error Pages
-----------

Invitation Followed
~~~~~~~~~~~~~~~~~~~

This page is shown when a user, who has already accepted an invitation,
follows the invitation link again.

Invitation Rejected
~~~~~~~~~~~~~~~~~~~

This page is shown when a user, who has already rejected an invitation,
follows the invitation link again.

Note about Forms
================
All forms submit to themselves, as the view handles the data, as it does
with the XForms in GroupServer 0.9. We always post, as almost all forms
have a side-effect.

