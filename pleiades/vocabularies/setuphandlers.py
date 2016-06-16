import logging
import os
import re

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from pleiades.vocabularies.interfaces import IPleiadesSettings
from imsvdex.vdex import VDEXManager

from Products.CMFCore.utils import getToolByName


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

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPleiadesSettings, False)

    for vocabname in vocab_names:
        vdexpath = os.path.join(
            os.path.dirname(__file__), 'data', '%s.vdex' % vocabname
            )
        try:
            f = open(vdexpath, 'r')
            data = f.read()
            f.close()
        except:
            logger.warn("Problems while reading VDEX import file " +
                        "provided at %s." % vdexpath)
            continue
        if vocabname != 'time-periods' and vocabname not in vocabs.contentIds():
            vid = vocabs.invokeFactory('PleiadesVocabulary', vocabname)
            wftool.doActionFor(vocabs[vid], action='publish')
            vdex = VDEXManager(data)
            for key in vdex.getVocabularyDict().keys():
                value = vdex.getTermCaptionById(key)
                descr = vdex.getTermDescriptionById(key).capitalize()
                tid = vocabs[vid].invokeFactory('PleiadesVocabularyTerm',
                                                key,
                                                title=value,
                                                description=descr)
                wftool.doActionFor(vocabs[vid][tid], action='publish')
            if vid in atvm.contentIds():
                atvm.manage_delObjects([vid])
            atvm.invokeFactory('AliasVocabulary', vid, target=vocabs[vid])
        if vocabname == 'time-periods':
            vdex = VDEXManager(data)
            settings.time_periods = []
            for key in vdex.getVocabularyDict().keys():
                value = vdex.getTermCaptionById(key)
                descr = vdex.getTermDescriptionById(key).capitalize()
                min = None
                max = None
                m = re.search(
                    r"\[\[(-{0,1}\d*\.{0,1}\d*)\s*,\s*(-{0,1}\d*\.{0,1}\d*)\]\]",
                    descr)
                if m is not None:
                    min = int(m.group(1))
                    max = int(m.group(2))
                settings.time_periods.append(dict(id=key,
                                                  title=value,
                                                  description=descr,
                                                  lower_bound=min,
                                                  upper_bound=max,
                                                  hidden=False))

    # prepopulate arch_remains vocab
    settings.arch_remains = []
    vocab_data = [{'id':'unknown', 'title':'Unknown'},
                  {'id':'none', 'title':'None'},
                  {'id':'traces', 'title':'Traces'},
                  {'id':'substantive', 'title':'Substantive'},
                  {'id':'restored', 'title':'Restored'},
                  {'id':'notvisible', 'title':'Not visible'}]
    for vocab_entry in vocab_data:
        settings.arch_remains.append(dict(id=vocab_entry['id'],
                                          title=vocab_entry['title']))

    return None


def install_datagrid_field(context):
    qi = getToolByName(context, 'portal_quickinstaller')
    if not qi.isProductInstalled('collective.z3cform.datagridfield'):
        qi.installProduct('collective.z3cform.datagridfield')
