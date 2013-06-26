# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.profile.invite',
    version=version,
    description="The user-profile pages on GroupServer that are "
      "required to accept invitations.",
    long_description=open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='sign up, registration, profile, user, join, invitation',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='http://groupserver.org',
    license='ZPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.profile'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pytz',
        'zope.cachedescriptors',
        'zope.component',
        'zope.contentprovider',
        'zope.formlib',
        'zope.interface',
        'zope.pagetemplate',
        'zope.publisher',
        'zope.schema',
        'Zope2',
        'gs.content.form',
        'gs.group.member.base',
        'gs.group.member.invite.base',
        'gs.group.member.join',
        'gs.profile.base',
        'gs.profile.email.base',
        'gs.profile.email.verify',
        'gs.profile.notify',
        'gs.profile.password',
        'Products.GSAuditTrail',
        'Products.CustomUserFolder',
        'Products.GSGroup',
        'Products.GSProfile',
        'Products.GSRedirect',
        'Products.XWFCore',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
