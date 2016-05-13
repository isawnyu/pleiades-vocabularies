import logging
import os

from imsvdex.vdex import VDEXManager

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException


logger = logging.getLogger('pleiades.configuration.setuphandlers')


def importVarious(context):
    """Miscellanous steps import handle."""
    if context.readDataFile('pleiades.vocabularies_various.txt') is None:
        return
    installVocabularies(context)
    

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    site = context.getSite()
    atvm = getToolByName(site, 'portal_vocabularies')
    wftool = getToolByName(site, 'portal_workflow')
    vocabs = site['vocabularies']
    vocab_names = [
        'name-accuracy',
        'association-certainty',
        'place-types',
        'attestation-confidence',
        'time-periods',
        'name-completeness',
        'ancient-name-languages',
        'name-types',
        ]
    for vocabname in vocab_names:
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
        if not vocabname in vocabs.contentIds():
            vid = vocabs.invokeFactory('PleiadesVocabulary', vocabname)
            try:
                wftool.doActionFor(vocabs[vid], action='publish')
            except WorkflowException:
                pass
            vdex = VDEXManager(data)
            for key in vdex.getVocabularyDict().keys():
                value = vdex.getTermCaptionById(key)
                descr = vdex.getTermDescriptionById(key).capitalize()
                tid = vocabs[vid].invokeFactory('PleiadesVocabularyTerm', key, title=value, description=descr)
                try:
                    wftool.doActionFor(vocabs[vid][tid], action='publish')
                except WorkflowException:
                    pass
            if vid in atvm.contentIds():
                atvm.manage_delObjects([vid])
            atvm.invokeFactory('AliasVocabulary', vid, target=vocabs[vid])
    return None
            