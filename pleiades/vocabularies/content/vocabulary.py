"""
A vocabulary is a container for key/value pairs.
This Vocabulary extends ATVM's SimpleVocabulary into workflowed user-space.
It exposes only published terms.
"""

from AccessControl import ClassSecurityInfo, getSecurityManager
from pleiades.vocabularies.config import PROJECTNAME
from pleiades.vocabularies.content.interfaces import IPleiadesVocabulary
from pleiades.vocabularies.content.interfaces import IPleiadesVocabularyTerm
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import DisplayList
from Products.Archetypes.utils import OrderedDict
from Products.ATVocabularyManager.config import *
from Products.ATVocabularyManager.types.simple.vocabulary import SimpleVocabulary
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
import re

SORT_METHOD_TEMPORAL = "Sort temporally (increasing date)"


class PleiadesVocabulary(SimpleVocabulary):
    implements(IVocabulary, IPleiadesVocabulary)

    security = ClassSecurityInfo()
    portal_type = meta_type = 'PleiadesVocabulary'
    archetype_name = 'PleiadesVocabulary'

    factory_type_information = {
        'allowed_content_types': ('PleiadesVocabularyTerm',),
        'allow_discussion': 1,
        'immediate_view': 'base_view',
        'global_allow': 1,
        'filter_content_types': 1,
        }

    _at_rename_after_creation = True

    schema = BaseFolderSchema + Schema((
        StringField(
            'id',
            required=1, ## Still actually required, but
                        ## the widget will supply the missing value
                        ## on non-submits
            mode="rw",
            accessor="getId",
            mutator="setId",
            default='',
            widget=StringWidget(
                label="Vocabulary Name",
                label_msgid="label_vocab_name",
                description="Should not contain spaces, underscores or mixed case.",
                description_msgid="help_vocab_name",
                i18n_domain="atvocabularymanager"
            ),
        ),

        TextField(
            'description',
            default='',
            required=0,
            searchable=0,
            accessor="Description",
            storage=MetadataStorage(),
            widget=TextAreaWidget(
                description="Enter a brief description",
                description_msgid="help_description",
                label="Description",
                label_msgid="label_description",
                rows=5,
                i18n_domain="plone",
            ),
        ),

        StringField(
            "sortMethod",
            default=SORT_METHOD_LEXICO_VALUES,
            required=0,  # smooth upgrades from 1.0.0-beta2
            searchable=0,
            widget=SelectionWidget(
                label="Sort method",
                label_msgid="label_sort_method",
                description="Sort method used for displaying vocabulary terms",
                description_msgid="help_sort_method",
                i18n_domain="atvocabularymanager",
            ),
            vocabulary=VOCABULARY_SORT_ORDERS + [SORT_METHOD_TEMPORAL]
        ),
    ))

    aliases = {
        '(Default)': 'base_view',
        'view': 'base_view',
        'edit': 'base_edit',
    }

    def getTermItems(self, all=False):
        """Securely get (key, value) tuples of published terms."""
        sm = getSecurityManager()
        return [
            (r.getTermKey(), r.getTermValue())
            for r in self.values()
            if IPleiadesVocabularyTerm.providedBy(r)
            and sm.checkPermission(View, r)
        ]

    def getDisplayList(self, instance):
        """Returns a object of class DisplayList as defined in
        Products.Archetypes.utils.

        The instance of the content class is given as parameter.
        The list is sorted accordingly to the sortMethod chosen.
        """
        dl = DisplayList()
        vdict = self.getVocabularyDict(instance)
        for key in self.getSortedKeys():
            dl.add(key, vdict[key])
        return dl

    def getVocabularyLines(self, instance=None):
        """Returns a List of Key-Value tuples.
        The list is sorted accordingly to the sortMethod chosen.
        """
        termlist = []
        vdict = self.getVocabularyDict(instance)

        for key in self.getSortedKeys():
            termlist.append((key, vdict[key]))
        return termlist

    def getVocabularyDict(self, instance=None, all=False):
        """Returns a vocabulary dictionary as defined in the interface, but
        only including published terms.
        """
        if self.isLinguaPloneInstalled():
            # if lp is installed
            # obtain language and return translated dict
            try:
                # we use the language of instance for this dictionary
                lang = instance.getLanguage()
            except AttributeError:
                # we retrieve the current language
                langtool = getToolByName(self, 'portal_languages')
                lang = langtool.getPreferredLanguage()
            return self._getTranslatedVocabularyDict(lang)
        else:
            # just return all terms
            vdict = OrderedDict()
            for k, v in self.getTermItems(all=all):
                vdict[k] = v
            return vdict

    def _getTranslatedVocabularyDict(self, lang):
        vdict = OrderedDict()
        for obj in self.contentValues():
            # we only use the canonical objects
            if obj.isCanonical():
                vdict[obj.getTermKey()] = obj.getTermValue(lang)
        return vdict

    def getSortedKeys(self):
        """ returns a list of keys sorted accordingly to the
        selected sort method (may be unsorted if method = no sort)
        """
        sortMethod = self.getSortMethod()
        keys, values = zip(*self.getTermItems())
        keys = list(keys)

        if not hasattr(self, 'sortMethod'):
            # smooth upgrade from previous releases
            return keys
        if sortMethod == SORT_METHOD_LEXICO_KEYS:
            keys.sort()
            return keys
        if sortMethod == SORT_METHOD_LEXICO_VALUES:
            # returns keys sorted by lexicogarphic order of VALUES
            sm = getSecurityManager()
            terms = [
                t for t in self.contentValues()
                if IPleiadesVocabularyTerm.providedBy(t)
                and sm.checkPermission(View, t)
            ]
            terms.sort(
                lambda x, y: cmp(
                    x.getVocabularyValue(), y.getVocabularyValue()))
            return [term.getVocabularyKey() for term in terms]
        if sortMethod == SORT_METHOD_FOLDER_ORDER:
            return keys
        if sortMethod == SORT_METHOD_TEMPORAL:
            sm = getSecurityManager()
            kvdict = dict(
                (k, t) for k, t in self.contentItems()
                if IPleiadesVocabularyTerm.providedBy(t)
                and sm.checkPermission(View, t)
            )

            def range(key):
                term = kvdict[key]
                descr = term.Description()
                m = re.search(
                    r"\[\[(-{0,1}\d*\.{0,1}\d*)\s*,\s*(-{0,1}\d*\.{0,1}\d*)\]\]",
                    descr)
                if m is not None:
                    min = float(m.group(1))
                    max = float(m.group(2))
                    return min, max
                else:
                    return None
            keys.sort(lambda x, y: cmp(range(x), range(y)))
        # fallback
        return keys


registerType(PleiadesVocabulary, PROJECTNAME)
