# Python imports
import re
import random

# Zope imports
from zope.interface import implements
from zope.event import notify

# Validation imports
from Products.validation.validators.BaseValidators import EMAIL_RE
        
# CMF imports
from Products.CMFCore.utils import getToolByName

from Products.eJSubscriptions.config import VALID, NOT_VALID, ALREADY_REGISTERED
from Products.eJSubscriptions.events import SubscriberAdded

VALID = u"You have successfully registered. Shortly you will get an activation \
        e-mail. Please follow its instructions to activate your registration."
NOT_VALID= u"Sorry, you have given an invalid e-mail address."
ALREADY_REGISTERED = u"Your e-mail address has already been registered."

ACTIVATED = u"Your registration has been activated. Thank you."
ALREADY_ACTIVATED = u"Your registration has already been activated"


class ParticipantManager:
    """Adapter which manages participant registration
    """    

    def __init__(self, context):
        """
        """
        self.context = context
        self.status_message = VALID
        
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
        #new_id = self._generateUniqueId()
        new_id = email ###XXX geht das???
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
        #notify(SubscriberAdded(subscriber))
               
        return True
        



    def get_participants(self):
        """
        """        
        return [s.getEmail() for  self.context.objectValues("WorkshopParticipant")]


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
        if email in self.get_participants():
            return True
        return False

    def _generateUniqueId(self):
        """
        """
        random.seed()        
        code = "".join([str(random.randint(0,9)) for i in range(0,20)])                           
        return code
