# -*- coding: utf-8 -*-
#

# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "zbw.ejWorkshop"

# Permissions
DEFAULT_ADD_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_PERMISSION, ('Manager', 'Owner'))

ADD_PERMISSIONS = {
    'WorkshopFolder' : 'zbw.ejWorkshop: Add Workshop Folder',
    'WorkshopParticipant' : 'zbw.ejWorkshop: Add Workshop Participant',
    
}


