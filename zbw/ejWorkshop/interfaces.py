from zope.interface import Interface
from zope import schema



class IParticipantAdded(Interface):
    """
    event marker interface
    """

class IParticipantActivated(Interface):
    """
    event marker interface
    """


class IParticipantManager(Interface):
    """
    storage and validation of participant registration
    """

class IWorkshopFolder(Interface):
    """
    Contenttype WorkshopFolder
    """

class IWorkshopParticipant(Interface):
    """
    Contenttype WorkshopParticipant
    """
    
    firstname = schema.TextLine(
            title=u'Firstname',
            required=True,
            )

    surname = schema.TextLine(
            title=u"Surname",
            required=True,
            )

    organisation = schema.TextLine(
            title=u"Organisation",
            required=True,
            )

    email = schema.TextLine(
            title=u"Email",
            required = True,
            )

    homepage = schema.TextLine(
            title=u"Homepage",
            description=u"URL of personal or institutional homepage",
            required=False,
            )

    postal = schema.Text(
            title=u"Postal Address",
            required=True
            )

    dinner = schema.Bool(
            title=u"Participation in the Workshop Dinner (at your own expense)",
            description=u"Dinner takes place at the restaurant 'Parlament'\
            (http://www.parlament-hamburg.de)",
            required=False
            )






    

    
