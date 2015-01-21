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

    text = """Dear <fullname>,

thank you for your request to register for the workshop "The Future of
Scholarly Communication in Economics".

To confirm your registration, please click on the following link:

<activate_url>

If you did not make this request, or it was made in error, please ignore this
email.

Many thanks,

The organizing team
(Workshop on The Future of Scholarly Communication in Economics)
"""


    message = text.replace("<email>", object.getEmail())
    message = message.replace("<activate_url>", "%s/confirm" % object.absolute_url())
    message = message.replace("<fullname>", object.getFullname())
        
    header  = "From: %s\n" % settings.notification_from
    header += "To: %s\n"  % object.getEmail()
    header += "Subject: %s\n" % u"Workshop Registration: please activate"
    header += "Content-Type: text/plain; charset=utf-8\n\n"

    mailtext = header+message
    object.MailHost.send(mailtext)
   

def mail_participant_activated(event):
    """
    """
    object = event.object

    text = """Dear <fullname>,

you've been successfully registered with your email address <email> to the
workshop "The Future of Scholarly Communication in Economics". 

This is your data:
    Firstname: <firstname>
    Surname: <surname>
    Organisation: <organisation>
    Email: <email>
    Homepage: <homepage>
    Postal Address: <postal>
    Dinner Participation: <dinner>

If you have any questions please send them to
editorial-office@economics-ejournal.org .

Many thanks,

The organizing team
(Workshop on The Future of Scholarly Communication in Economics)
"""
    

    message = text.replace("<fullname>", object.getFullname())
    message = message.replace("<email>", object.getEmail())
    message = message.replace("<firstname>", object.getFirstname())
    message = message.replace("<surname>", object.getSurname())
    message = message.replace("<organisation>", object.getOrganisation())
    message = message.replace("<postal>", object.getPostal())

    if object.getHomepage():
        message = message.replace("<homepage>", object.getHomepage())
    else:
        message = message.replace("<homepage>", "None")

    if object.getDinner():
        message = message.replace("<dinner>", "Yes")
    else:
        message = message.replace("<dinner>", "No")

    
    header  = "From: %s\n" % settings.notification_from
    header += "To: %s\n"  % object.getEmail()
    header += "Subject: Workshop registration successful\n"
    header += "Content-Type: text/plain; charset=utf-8\n\n"
    message = header + message
    
    object.MailHost.send(message)
