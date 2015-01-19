import re
import random
from zope.event import notify
from Products.validation.validators.BaseValidators import EMAIL_RE
from Products.CMFCore.utils import getToolByName

from zbw.ejWorkshop.events import ParticipantAdded, ParticipantActivated


VALID = u"You have successfully registered. Shortly you will get an activation \
        e-mail. Please follow its instructions to activate your registration."
NOT_VALID= u"Sorry, you have given an invalid e-mail address."
ALREADY_REGISTERED = u"The given e-mail address has already been registered."

ACTIVATED = u"Your registration has been activated. We have sent you an email \
            with the confirmation as well as further information"
ALREADY_ACTIVATED = u"Your registration has already been activated"


class ParticipantManager:
    """Adapter which manages participant registration
    """    

    def __init__(self, context):
        """
        """
        self.context = context
        self.status_message = VALID
        self.status=""
        
    def add(self, data):
        """Adds a participant
        """
        
        email = data['email']

        # check
        if self._isValid(email) == False:
            self.status_message = NOT_VALID
            return False

        # Normalize E-Mail
        email = email.lower()

        if self._isAlreadyRegistered(email) == True:
            self.status_message = ALREADY_REGISTERED
            return False
        
        # Add Subscriber
        id_random = self._generateUniqueId()
        new_id = email + '_' + id_random  #email for simpler identification in folder list
        self.context.invokeFactory(id=new_id, type_name="WorkshopParticipant")
        participant = getattr(self.context, new_id)
        
        participant.setEmail(email)
        participant.setFirstname(data['firstname'])
        participant.setSurname(data['surname'])
        participant.setOrganisation(data['organisation'])
        participant.setDinner(data['dinner'])
        
        if data['homepage']:
            participant.setHomepage(data['homepage'])

        if data['postal']:
            participant.setPostal(data['postal'])

        participant.reindexObject()        

        # send added event
        notify(ParticipantAdded(participant))
               
        return True
        

    def activate(self):
        """
        Activates a participant
        """
        wftool = getToolByName(self.context, "portal_workflow")

        review_state = wftool.getInfoFor(self.context, "review_state")
        if review_state == "waiting":
            wftool.doActionFor(self.context, "activate")
            notify(ParticipantActivated(self.context))
            self.status = ACTIVATED                        
        elif review_state == "active":
            self.status = ALREADY_ACTIVATED            


    def _get_participants(self):
        """
        """        
        return [s.getEmail() for s in self.context.objectValues("WorkshopParticipant")]


    def _isValid(self, email):
        """
        """
        mo = re.search(EMAIL_RE, email)
                
        if mo is None:
            return False
        
        return True
            
    def _isAlreadyRegistered(self, email):
        """
        """    
        if email in self._get_participants():
            return True
        return False

    def _generateUniqueId(self):
        """
        """
        random.seed()        
        code = "".join([str(random.randint(0,9)) for i in range(0,20)])                           
        return code



