import logging
import os
import re

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.registry.interfaces import IRegistry
from pleiades.vocabularies.interfaces import IPleiadesSettings
from pleiades.vocabularies.content.interfaces import IPleiadesVocabularyFolder
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
    vocab_folder = site['vocabularies']
    atvm_vocabs = [
        'name-accuracy',
        'association-certainty',
        'place-types',
        'attestation-confidence',
        'name-completeness',
        'ancient-name-languages',
        'name-types',
        'time-periods',
        ]
    registry_vocabs = [
        'time-periods',
        'place-types',
    ]

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPleiadesSettings, False)

    for vocabname in (atvm_vocabs + registry_vocabs):

        # Read from .vdex file
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

        if vocabname in atvm_vocabs and vocabname not in vocab_folder.contentIds():
            vid = vocab_folder.invokeFactory('PleiadesVocabulary', vocabname)
            try:
                wftool.doActionFor(vocab_folder[vid], action='publish')
            except WorkflowException:
                pass
            vdex = VDEXManager(data)
            for key in vdex.getVocabularyDict().keys():
                value = vdex.getTermCaptionById(key)
                descr = vdex.getTermDescriptionById(key).capitalize()
                tid = vocab_folder[vid].invokeFactory(
                    'PleiadesVocabularyTerm', key,
                    title=value, description=descr)
                try:
                    wftool.doActionFor(vocab_folder[vid][tid], action='publish')
                except WorkflowException:
                    pass
            if vid in atvm.contentIds():
                atvm.manage_delObjects([vid])
            atvm.invokeFactory('AliasVocabulary', vid, target=vocab_folder[vid])

        elif vocabname in registry_vocabs:
            vocabkey = vocabname.replace('-', '_')

            # Avoid overwriting existing terms
            value = getattr(settings, vocabkey, None)
            if value is not None:
                continue

            vdex = VDEXManager(data)
            terms = []
            for key in vdex.getVocabularyDict().keys():
                title = vdex.getTermCaptionById(key)
                descr = vdex.getTermDescriptionById(key).capitalize()
                term = dict(
                    id=key.decode('utf8'),
                    title=title.decode('utf8'),
                    description=descr.decode('utf8'),
                    hidden=False,
                    same_as=None,
                )
                if vocabname == 'time-periods':
                    min = None
                    max = None
                    m = re.search(
                        r"\[\[(-{0,1}\d*\.{0,1}\d*)\s*,\s*(-{0,1}\d*\.{0,1}\d*)\]\]",
                        descr)
                    if m is not None:
                        min = int(m.group(1))
                        max = int(m.group(2))
                    term['lower_bound'] = min
                    term['upper_bound'] = max
                terms.append(term)
            setattr(settings, vocabkey, terms)

    # prepopulate arch_remains vocab - if uninitialized
    if not settings.arch_remains:
        settings.arch_remains = [
            {'id': u'unknown', 'title': u'Unknown'},
            {'id': u'none', 'title': u'None'},
            {'id': u'traces', 'title': u'Traces'},
            {'id': u'substantive', 'title': u'Substantive'},
            {'id': u'restored', 'title': u'Restored'},
            {'id': u'notvisible', 'title': u'Not visible'},
        ]

    # prepopulate relationship_types vocab - if uninitialized
    if not settings.relationship_types:
        settings.relationship_types = [
            {'id': u'connection', 'title': u'connection', 'description': u'',
             'same_as': None, 'hidden': False},
            {'id': u'at', 'title': u'at', 'description': u'',
             'same_as': None, 'hidden': False},
            {'id': u'on', 'title': u'on', 'description': u'',
             'same_as': None, 'hidden': False},
            {'id': u'part_of_admin', 'title': u'part of (administrative)',
             'description': u'', 'same_as': None, 'hidden': False},
            {'id': u'part_of_regional', 'title': u'part of (regional)',
             'description': u'', 'same_as': None, 'hidden': False},
            {'id': u'near', 'title': u'near', 'description': u'',
             'same_as': None, 'hidden': False},
            {'id': u'intersects', 'title': u'intersects', 'description': u'',
             'same_as': None, 'hidden': False},
        ]


def install_datagrid_field(context):
    qi = getToolByName(context, 'portal_quickinstaller')
    if not qi.isProductInstalled('collective.z3cform.datagridfield'):
        qi.installProduct('collective.z3cform.datagridfield')


def remove_old_time_periods(context):
    ut = getToolByName(context, 'portal_url')
    site = ut.getPortalObject()
    vocabs = site['vocabularies']
    if 'time-periods' in vocabs.objectIds():
        vocabs.manage_delObjects(['time-periods'])
        # apply marker interface so that new views can only be used here
        alsoProvides(vocabs, IPleiadesVocabularyFolder)
        # change default view to point to our custom folder listing
        vocabs.setLayout('pleiades-vocabulary-listing')


def migrate_place_types(context):
    pass
