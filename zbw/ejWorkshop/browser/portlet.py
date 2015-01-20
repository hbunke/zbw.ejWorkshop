from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from plone.memoize.instance import memoize


class View(BrowserView):
    """
    """

    @memoize
    def folder_content(self):
        """
        returns all pages inside the workshop folder
        """
        if self.context.portal_type=="WorkshopFolder":
            root = self.context
        else:
            root = self.context.aq_inner.aq_parent

        folder_path = '/'.join(root.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(path={'query': folder_path, 'depth' : 1},
                portal_type="Document")
        content = [brain.getObject() for brain in brains]
        return content

    
    def isManager(self):
        """
        """
        return getSecurityManager().checkPermission('Manage portal',
                self.context)

    
    def root(self):
        """
        """
        if self.context.portal_type=="WorkshopFolder":
            return self.context.absolute_url()

        else:
            return self.context.aq_inner.aq_parent.absolute_url()

    
    @memoize
    def news(self):
        """
        """
        #catalog = getToolByName(self, 'portal_catalog')
        #brains = catalog(portal_type="News Item", sort_on='created',
        #        sort_order='reverse', Subject='workshop2015')
        
        if self.context.portal_type=="WorkshopFolder":
            root = self.context
        else:
            root = self.context.aq_inner.aq_parent

        folder_path = '/'.join(root.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(path={'query': folder_path, 'depth' : 1},
                portal_type="News Item")

        return [brain.getObject() for brain in brains]
