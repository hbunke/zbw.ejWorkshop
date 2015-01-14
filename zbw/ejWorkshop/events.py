from zope.interface import Interface, implements


#XXX interfaces in .interfaces.py?
class IParticipantAdded(Interface):
    """
    marker interface
    """

class IParticipantActivated(Interface):
    """A marker interface
    """


class ParticipantAdded(object):
    """An Event, which is triggered when a participant has been added.
    """
    implements(IParticipantAdded)
    
    def __init__(self, object):
        self.object = object        

    
class ParticipantActivated(object):
    """
    An Event, which is triggered when a participant is activated
    """
    implements(IParticipantActivated)
    
    def __init__(self, object):
        self.object = object      
                

# Subscribers        

def sendAddedMail(event):
    """
    """
    object = event.object

    registry = getUtility(IRegistry)
    stool = registry.forInterface(ISubscriptionsConf)

    message = stool.added_subscriber_email.encode('utf-8')
    message = message.replace("<email>", object.getEmail())
    message = message.replace("<activate_url>", "%s/activate" % object.absolute_url())
        
    header  = "From: %s\n" % settings.notification_from
    header += "To: %s\n"  % object.getEmail()
    header += "Subject: %s\n" % stool.added_subscriber_subject.encode('utf-8')
    header += "Content-Type: text/plain; charset=utf-8\n\n"

    mailtext = header+message
    object.MailHost.send(mailtext)
   

def sendActivatedMail(event):
    """
    """
    object = event.object

    registry = getUtility(IRegistry)
    stool = registry.forInterface(ISubscriptionsConf)

    message = stool.activated_subscriber_email.encode('utf-8')
    
    message = message.replace("<email>", object.getEmail())
    message = message.replace("<edit_url>", object.absolute_url())
    message = message.replace("<delete_url>", "%s/delete" % object.absolute_url())
    
    header  = "from: %s\n" % settings.notification_from
    header += "to: %s\n"  % object.getEmail()
    header += "subject: %s\n" %  stool.activated_subscriber_subject.encode('utf-8')
    header += "Content-Type: text/plain; charset=utf-8\n\n"
    message = header + message
    
    object.MailHost.send(message)
