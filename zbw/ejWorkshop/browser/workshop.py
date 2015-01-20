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
from plone.memoize.instance import memoize
from zbw.ejWorkshop.interfaces import IWorkshopParticipant, IParticipantManager
from zope.app.form.browser import TextAreaWidget as _TextAreaWidget


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
    
    template = ViewPageTemplateFile("participants.pt")

    def __call__(self):
        #self.request.set('disable_border', True)
        return self.template()


    @memoize
    def get_active_participants(self):
        """
        returns a list of confirmed participants
        """
        #TODO: as soon as we have a second workshop we also have to query the
        #path or any arbituary other ID!
        catalog = getToolByName(self, "portal_catalog")                    
        brains = catalog(portal_type="WorkshopParticipant",
                        review_state="active")
        
        return [brain.getObject() for brain in brains]


    @memoize
    def get_waiting_participants(self):
        """
        returns a list of unconfirmed participants
        """
        
        #TODO: as soon as we have a second workshop we also have to query the
        #path or any arbituary other ID!
        catalog = getToolByName(self, "portal_catalog")                    
        brains = catalog(portal_type="WorkshopParticipant",
                        review_state="waiting")
        
        return [brain.getObject() for brain in brains]

    
    def get_dinner_participants(self):
        """
        """
        participants = self.get_active_participants()
        no = 0
        for p in participants:
            if p.getDinner() is True:
                no+=1
        return no



#see http://docs.plone.org/old-reference-manuals/formlib/customtemplate.html 
#for this approach to customize formlib widgets
def TextAreaWidget(field, request):
    widget = _TextAreaWidget(field, request)
    widget.height = 5
    widget.width = 40
    return widget

class ParticipantForm(PageForm):
    """
    using zope.formlib
    """
    form_fields = form.Fields(IWorkshopParticipant)
    #result_template = ViewPageTemplateFile('feedback_result.pt')

    label = u"Workshop Registration"
    form_fields['postal'].custom_widget = TextAreaWidget

    @form.action("Register")
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

    
class Participant(BrowserView):
    """
    participant management
    """

    def confirm(self):
        """
        """
        pm = IParticipantManager(self.context)
        pm.activate()
        status = pm.status
        
        self.context.plone_utils.addPortalMessage(status)
        url = self.aq_inner.aq_parent.aq_parent.absolute_url()
        return self.request.response.redirect(url)


