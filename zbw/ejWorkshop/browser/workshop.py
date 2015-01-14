# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics (ZBW)
# http://zbw.eu/

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.interface import Interface
#from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from five.formlib.formbase import PageForm
from zope.formlib import form

from zbw.ejWorkshop.interfaces import IWorkshopParticipant, IParticipantManager

class FolderView(BrowserView):
    """
    custom view for workshop
    """

    template = ViewPageTemplateFile("workshop_view.pt")

    def __call__(self):
        #self.request.set('disable_border', True)
        return self.template()


class ParticipantsView(BrowserView):
    """
    custom view for workshop participants
    """
    
    template = ViewPageTemplateFile("workshop_participants.pt")

    def __call__(self):
        #self.request.set('disable_border', True)
        return self.template()


    def get_participants(self):
        """
        returns a sorted list of all participants
        """
        #TODO: as soon as we have a second workshop we also have to query the
        #path or any arbituary other ID!
        catalog = getToolByName(self, "portal_catalog")                    
        brains = catalog(portal_type="WorkshopParticipant")
        
        return [brain.getObject() for brain in brains]


#class ParticipantForm(BrowserView):
#   """
#   without any form framework
#   """
#   
#   template = ViewPageTemplateFile("regform.pt")

#   def __call__(self):
#       #self.request.set('disable_border', True)
#       return self.template()

class ParticipantForm(PageForm):
    """
    using zope.formlib
    """
    form_fields = form.Fields(IWorkshopParticipant)
    #result_template = ViewPageTemplateFile('feedback_result.pt')

    label = u"Workshop Registration"

    @form.action("register")
    def register(self, action, data):
        """
        calling an adapter to store participant data
        """
        
        folder = self.context
        manager = IParticipantManager(folder)
        manager.add(data)
        
        message = manager.status_message
        self.context.plone_utils.addPortalMessage(message)
        url  = self.context.absolute_url()
        self.request.response.redirect(url)

    
    

