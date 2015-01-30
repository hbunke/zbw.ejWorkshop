from zope.interface import implements
from zope.component import getUtility
from zbw.ejWorkshop.interfaces import IParticipantAdded, IParticipantActivated
from Products.eJournal import settings



class ParticipantAdded(object):
    """An Event, which is triggered when a participant has been added.
    """
    implements(IParticipantAdded)
    
    def __init__(self, object):
        self.object = object        

    
class ParticipantActivated(object):
    """
    triggered when a participant is activated
    """
    implements(IParticipantActivated)
    
    def __init__(self, object):
        self.object = object      
                

# Subscribers        

def mail_participant_added(event):
    """
    """
    object = event.object

    text = u"""Dear <firstname> <surname>,

thank you for your request to register for the workshop "The Future of Scholarly Communication in Economics".

To confirm your registration, please click on the following link:

<activate_url>

If you did not make this request, or it was made in error, please ignore this email.

Many thanks,

The organizing team
(Workshop on The Future of Scholarly Communication in Economics)
"""

    surname = object.getSurname()
    surname = surname.decode('utf-8')
    #surname = surname.encode('utf-8')

    firstname = object.getFirstname()
    firstname = firstname.decode('utf-8')
    #firstname = firstname.encode('utf-8')

    message = text.replace("<email>", object.getEmail())
    message = message.replace("<activate_url>", "%s/confirm" % object.absolute_url())
    message = message.replace("<firstname>", firstname)
    message = message.replace("<surname>", surname)        
    header  = u"From: %s\n" % settings.notification_from
    header += u"To: %s\n"  % object.getEmail()
    header += u"Subject: %s\n" % u"Workshop Registration: please activate"
    header += u"Content-Type: text/plain; charset=utf-8\n\n"

    mailtext = header+message
    object.MailHost.send(mailtext, encode="utf-8", charset="utf-8")
   

def mail_participant_activated(event):
    """
    """
    object = event.object

    text = u"""Dear <firstname> <surname>,

you've been successfully registered with your email address <email> to the workshop "The Future of Scholarly Communication in Economics". 

This is your data:
    Firstname: <firstname>
    Surname: <surname>
    Organisation: <organisation>
    Email: <email>
    Homepage: <homepage>
    Postal Address: <postal>
    Dinner Participation: <dinner>

If you have any questions please send them to editorial-office@economics-ejournal.org .

Many thanks,

The organizing team
(Workshop on The Future of Scholarly Communication in Economics)
"""
    
    
    message = text.replace("<email>", object.getEmail())
    message = message.replace("<firstname>", object.getFirstname().decode('utf-8'))
    message = message.replace("<surname>", object.getSurname().decode('utf-8'))        
    message = message.replace("<organisation>", object.getOrganisation().decode('utf-8'))
    message = message.replace("<postal>", object.getPostal().decode('utf-8'))

    if object.getHomepage():
        message = message.replace("<homepage>", object.getHomepage())
    else:
        message = message.replace("<homepage>", u"None")

    if object.getDinner():
        message = message.replace("<dinner>", u"Yes")
    else:
        message = message.replace("<dinner>", u"No")

    
    header  = u"From: %s\n" % settings.notification_from
    header += u"To: %s\n"  % object.getEmail()
    header += u"Subject: Workshop registration successful\n"
    header += u"Content-Type: text/plain; charset=utf-8\n\n"
    message = header + message
    
    object.MailHost.send(message, encode="utf-8", charset="utf-8")

