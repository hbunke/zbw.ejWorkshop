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
from zope.app.form.browser import TextWidget as _TextWidget
from AccessControl import getSecurityManager



class FolderView(BrowserView):
    """
    custom view for workshop
    """

    template = ViewPageTemplateFile("workshop_view.pt")

    def __call__(self):
        
        is_manager =getSecurityManager().checkPermission('Manage portal', self.context)
        if not is_manager:
            self.request.set('disable_border', True)
        return self.template()


class ParticipantsView(BrowserView):
    """
    custom view for workshop participants
    """
    
    template = ViewPageTemplateFile("participants.pt")

    def __call__(self):
        self.request.set('disable_border', True)
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
                        review_state="active",
                        sort_on="created", sort_order="descending")
        
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
                        review_state="waiting",
                        sort_on="created", sort_order="ascending")
        
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

def TextWidgetLarge(field, request):
    widget = _TextWidget(field, request)
    widget.displayWidth = 50
    return widget

class ParticipantForm(PageForm):
    """
    using zope.formlib
    """
    form_fields = form.Fields(IWorkshopParticipant)
    #result_template = ViewPageTemplateFile('feedback_result.pt')
    
    #see http://docs.plone.org/old-reference-manuals/formlib/customtemplate.html
    template = ViewPageTemplateFile('pageform.pt')
    label = u"Workshop Registration"
    description=u''
    form_fields['postal'].custom_widget = TextAreaWidget
    form_fields['homepage'].custom_widget = TextWidgetLarge

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


    def full(self):
        """
        checks for number of participants
        """
        full = 38
        catalog = getToolByName(self, "portal_catalog")                    
        brains = catalog(portal_type="WorkshopParticipant",
                        review_state="active",
                        sort_on="created", sort_order="descending")
        uptonow = len(brains)
        if uptonow >= full:
            return True
        return False


    
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



