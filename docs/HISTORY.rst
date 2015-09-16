Changelog
=========

4.0.4 (2015-09-15)
------------------

* ``s/Dear/Hello/g`` in the notifications
* Naming the reStructuredText files as such
* Pointing at `GitHub`_ as the primary code repository

.. _GitHub: https://github.com/groupserver/gs.profile.invite

4.0.3 (2014-06-11)
------------------

* Fixing the heading in the *Invitation declined* notification
* Following the form-code to `gs.content.form.base`_

.. _gs.content.form.base:
   https://github.com/groupserver/gs.content.form.base

4.0.2 (2014-02-28)
------------------

* Further ``Content-type`` fixes

4.0.1 (2014-02-20)
------------------

* Ensuring the ``Content-type`` header is set correctly
* Switching to Unicode literals

4.0.0 (2013-10-11)
------------------

* Using the ``gs.content.email.*`` style notification messages
* Ensuring members cannot join a group

3.0.1 (2013-09-23)
------------------

* Recomputing the current invitations, closing `Bug 3864`_

.. _Bug 3864: https://redmine.iopen.net/issues/3864

3.0.0 (2013-07-12)
------------------

* Updating the UI

2.7.0 (2013-06-26)
------------------

* Adding a password toggle
* Adding WAI-ARIA support
* Cleaning up the code

2.6.1 (2012-07-12)
------------------

* Improving the URLs
* Using a more standard style for the *Respond* page

2.6.0 (2012-07-05)
------------------

* Dropping the context menu
* Using a better redirect for the invited member
* Using relative URLs

2.5.3 (2012-06-22)
------------------

* Update for SQLAlchemy

2.5.2 (2012-05-15)
------------------

* Following `gs.group.member.invite.base`_

.. _gs.group.member.invite.base:
   https://github.com/groupserver/gs.group.member.invite.base

2.5.1 (2012-02-09)
------------------

* Improving the performance of the page
* Fixing some text

2.5.0 (2011-02-23)
------------------

* Setting the context for the *Privacy* context provider
* Getting the *Accept* button and *Decline* button looking correct

2.4.7 (2011-01-26)
------------------

* Refactoring for `gs.profile.email.base`_

.. _gs.profile.email.base:
   https://github.com/groupserver/gs.profile.email.base

2.4.6 (2011-01-12)
------------------

* Removing an extra ``/``

2.4.5 (2011-01-01)
------------------

* Following the code in `gs.profile.email.verify`_

.. _gs.profile.email.verify:
   https://github.com/groupserver/gs.profile.email.verify


2.4.4 (2010-12-15)
------------------

* Moving the page-specific styles to the global stylesheet
* Using the new form-message content provider

2.4.3 (2010-11-23)
------------------

* Using the new ``gs.content.form.SiteForm``
* Following the password code to `gs.profile.password`_

.. _gs.profile.password:
   https://github.com/groupserver/gs.profile.password

2.4.2 (2010-10-05)
------------------

* Updating the wording on the *Initial response* page
* Registering the audit factory

2.4.1 (2010-09-23)
------------------

* Switching to the correct *Response* page depending on the
  presence or absence of a verified email address

2.4.0 (2010-09-07)
------------------

* Skipping the groups the person is already a member of
* Handling invitations from the wrong site
* Redirecting to the correct site

2.3.2 (2010-08-19)
------------------

* Improving the robustness

2.3.1 (2010-08-04)
------------------

* Adding an ``assert``

2.3.0 (2010-07-29)
------------------

* Moving code to ``gs.group.member.invite``
* Moving code to ``gs.group.member.join``
* Updating the auditing

2.2.1 (2010-07-21)
------------------

* Improving the link to the *Response* page
* Fixing a typing error
* Cleaning up the code

2.2.0 (2010-07-05)
------------------

* Verifying the address when the invitation is accepted.
* Adding error pages

2.1.0 (2010-07-01)
------------------

* Moving the *Respond* page here from ``GSGroupMember``
* Providing more information about the group

2.0.0 (2010-06-09)
------------------

* Moving the group-code to ``gs.group.member.invite``

1.0.0 (2010-04-23)
------------------

Initial version, based on `gs.profile.signup`_

.. _gs.profile.signup: https://github.com/github/gs.profile.signup
