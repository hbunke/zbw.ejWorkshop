## workshop content types

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from AccessControl import ClassSecurityInfo

from zbw.ejWorkshop.interfaces import IWorkshopFolder, IWorkshopParticipant
from zbw.ejWorkshop.config import PROJECTNAME


WorkshopFolderSchema = atapi.BaseFolderSchema.copy() + atapi.Schema((

    atapi.StringField('title',
        required=True,
        widget=atapi.StringWidget(
            label=u"Workshop Title",
            description=u"",
            ),
       ),


    atapi.TextField('introduction',
        widget=atapi.RichWidget(
            label=u"Introduction Text",
            ),
        ),

))



WorkshopParticipantSchema = atapi.BaseSchema.copy() + atapi.Schema((

     atapi.StringField(
        name='firstname',
        widget=atapi.StringWidget(
            label=u'Firstname',
        ),
        required=1
    ),

    atapi.StringField(
        name='surname',
        widget=atapi.StringWidget(
            label=u'Surname',
        ),
        required=1
    ),

    atapi.StringField(
        name='organisation',
        widget=atapi.StringWidget(
            label=u'Organisation',
        ),
        required=1
    ),


    atapi.StringField(
        name='email',
        required=1,
        widget=atapi.StringWidget(
            label=u'Email',
        )
    ),

    atapi.StringField(
        name="homepage",
        widget=atapi.StringWidget(
            label=u"Homepage",
            description=u"URL of personal or institutional homepage",
            ),
    ),

    atapi.TextField(
        name="postal",
        widget=atapi.TextAreaWidget(
            label="Postal Addresse",
        )
    ),

    atapi.BooleanField(
        name="dinner",
        widget=atapi.BooleanWidget(
            label=u"Participation in the Workshop Dinner (at your own expense)",
            description=u"Dinner takes place at the restaurant 'Parlament'\
            (http://www.parlament-hamburg.de)",
            ),
        ),

))



class WorkshopFolder(atapi.BaseFolder):
    """
    Workshop folder
    """
    implements(IWorkshopFolder)
    security = ClassSecurityInfo()

    portal_type = "WorkshopFolder"
    _at_rename_after_creation = True
    schema = WorkshopFolderSchema


class WorkshopParticipant(atapi.BaseContent):
    """
    register Workshop Participant
    """

    security = ClassSecurityInfo()
    
    implements(IWorkshopParticipant)

    _at_rename_after_creation = False
    schema = WorkshopParticipantSchema
    portal_type = "WorkshopParticipant"

    schema["title"].required = False
    schema["title"].widget.visible = {"edit": "invisible", "view": "invisible"}

    
    def getFullname(self):
        """For the catalog.
        """
        #return self.Title()

        fullname = u""
        surname = self.getSurname()
        firstname = self.getFirstname()
        
        if firstname != "":
            fullname += firstname
        if surname != "":
            fullname += u" %s" %surname

        return fullname

    def getTitle(self):
        """
        """
        return self.getFullname()
    
 
#class WorkshopParticipants(atapi.BaseFolder):
#   """
#   folder for collecting workshop participants
#   """
#   security = ClassSecurityInfo()
#   implements(IWorkshopParticipants)
#   _at_rename_after_creation = True
#   schema = atapi.BaseFolderSchema.copy()
#   portal_type = "WorkshopParticipants"


atapi.registerType(WorkshopFolder, PROJECTNAME)
#atapi.registerType(WorkshopParticipants, PROJECTNAME)
atapi.registerType(WorkshopParticipant, PROJECTNAME)

