# coding=utf-8
from zope.app.apidoc.interface import getFieldsInOrder
from Products.GSProfile import interfaces

class InviteFields(object)
    def __init__(self, context):
        self.context = context
        self.__profileFieldIds = self.__profileFields =  None
        self.__adminWidgets = self.__adminInterface = None
        self.__widgetNames = None

    @property
    def config(self):
        if self.__config == None:
            site_root = self.context.site_root()
            assert hasattr(site_root, 'GlobalConfiguration')
            self.__config = site_root.GlobalConfiguration
        return self.__config
        
    @property
    def adminInterface(self):
        if self.__adminInterface == None:
            adminInterfaceName = '%sAdminJoinSingle' %\
                self.config.getProperty('profileInterface', 'IGSCoreProfile')
            assert hasattr(interfaces, adminInterfaceName), \
                'Interface "%s" not found.' % adminInterfaceName
            self.__adminInterface = getattr(interfaces, adminInterfaceName)
        return self.__adminInterface
        
    def get_admin_widgets(self, widgets):
        '''These widgets are specific to the Invite a New Member 
            interface. They form the first part of the form.'''
        if self.__adminWidgets == None:
            sfIds = self.profileFieldIds
            adminWidgetIds = \
                ['form.%s' % f[0] 
                    for f in getFieldsInOrder(self.adminInterface)
                    if f[0] not in sfIds]
            self.__adminWidgets = [w for w in widgets
                                    if w.name in adminWidgetIds]
        assert self.__adminWidgets
        return self.__adminWidgets

    @property
    def profileInterface(self):
        if self.__interface == None:
            interfaceName =\
                self.config.getProperty('profileInterface', 'IGSCoreProfile')
            assert hasattr(interfaces, interfaceName), \
                'Interface "%s" not found.' % interfaceName
            self.__interface = getattr(interfaces, interfaceName)
        return self.__interface
        
    @property
    def profileFieldIds(self):
        if self.__profileFields == None:
            self.__profileFields = \
                [f[0] for f in getFieldsInOrder(self.profileInterface)]
        assert type(self.__profileFields) == list
        return self.__profileFields

    @property
    def profileWidgets(self):
        '''These widgets are the standard profile fields for this site.
            They form the second-part of the form.'''
        profileWidgetIds = ['form.%s' % i for i in self.profileFieldIds]
        retval = [w for w in self.widgets if w.name in profileWidgetIds]
        return retval

