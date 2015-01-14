from zope.interface import Interface
from zope import schema



class IParticipantManager(Interface):
    """
    manages storage and validation of participant registration
    """

class IWorkshopFolder(Interface):
    """
    Interface for contenttype WorkshopFolder
    """

class IWorkshopParticipant(Interface):
    """
    Interface for Workshop Participant
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






    

    
