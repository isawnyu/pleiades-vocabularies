import logging
import os

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('pleiades.configuration.setuphandlers')

def importVarious(context):
    """Miscellanous steps import handle
    """
    
    if context.readDataFile('pleiades.vocabularies_various.txt') is None:
        return
    installVocabularies(context)
    
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
            atvm.invokeFactory(vocabmap[vocabname][0], vocabname)
            atvm[vocabname].importXMLBinding(data)
            