import os

# from zope.event import notify
# from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
# 
# from App.Common import package_home
from Products.CMFCore.utils import getToolByName
#from Products.ATVocabularyManager.types.vdex import IMSVDEXVocabulary

def importVarious(context):
    """Miscellanous steps import handle
    """
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('pleiades.vocabularies_various.txt') is None:
        return
    installVocabularies(context)
    
# def addIMSVDEXVocabulary(context, id, **kwargs):
#     obj = IMSVDEXVocabulary(id)
#     dummy = '<?xml version="1.0" encoding="UTF-8"?>\n<vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0"\n     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n    xsi:schemaLocation="http://www.imsglobal.org/xsd/imsvdex_v1p0 imsvdex_v1p0_thesaurus.xsd"\n    profileType="thesaurus" language="en" orderSignificant="false">\n    \n    <vocabName>\n        <langstring language="en">Levels of Attestation Accuracy for Historical Names Distinguished in AWMC Publications</langstring>\n    </vocabName>\n    \n    <vocabIdentifier isRegistered="false">name-accuracy</vocabIdentifier>\n</vdex>'
#     obj.getField('vdex').set(obj, dummy)
#     notify(ObjectCreatedEvent(obj))
#     context._setObject(id, obj)
#     obj = context._getOb(id)
#     obj.initializeArchetype(**kwargs)
#     obj.portal_type = 'VdexVocabulary'
#     notify(ObjectModifiedEvent(obj))
#     return obj.getId()

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    site = context.getSite()
    # Create vocabularies in vocabulary lib
    atvm = getToolByName(site, 'portal_vocabularies')
    vocabmap = {'name-accuracy': ('VdexVocabulary', 'VdexTerm'),
         'association-certainty': ('VdexVocabulary', 'VdexTerm'),
         'place-types': ('VdexVocabulary', 'VdexTerm'),
         'attestation-confidence': ('VdexVocabulary', 'VdexTerm'),
         'time-periods': ('VdexVocabulary', 'VdexTerm'),
         'name-completeness': ('VdexVocabulary', 'VdexTerm'),
         'ancient-name-languages': ('VdexVocabulary', 'VdexTerm'),
         'name-types': ('VdexVocabulary', 'VdexTerm'),
        }
    for vocabname in vocabmap.keys():
        vdexpath = os.path.join(
            os.path.dirname(__file__), 'data', '%s.vdex' % vocabname
            )
        try:
            f = open(vdexpath, 'r')
            data = f.read()
            f.close()
        except:
            logger.warn("Problems while reading VDEX import file "+\
                        "provided at %s." % vdexpath)
            continue
        if not vocabname in atvm.contentIds():
            #addIMSVDEXVocabulary(atvm, vocabname, vdex=data)
            atvm.invokeFactory(vocabmap[vocabname][0], vocabname)
            atvm[vocabname].importXMLBinding(data)
        # if len(atvm[vocabname].contentIds()) < 1:
        #     if vocabmap[vocabname][0] == "VdexVocabulary":
        #         if not (os.path.exists(vdexpath) and os.path.isfile(vdexpath)):
        #             logger.warn('No VDEX import file provided at %s.' % vdexpath)
        #             continue
        #         try:
        #             #read data
        #             f = open(vdexpath, 'r')
        #             data = f.read()
        #             f.close()
        #         except:
        #             logger.warn("Problems while reading VDEX import file "+\
        #                         "provided at %s." % vdexpath)
        #             continue
        #         # this might take some time!
        #         atvm[vocabname].setVdex(data) #importXMLBinding(data)
        #     else:
        #         pass