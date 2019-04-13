
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from pleiades.vocabularies.interfaces import IPleiadesSettings
from pleiades.vocabularies.tests.base import PleiadesVocabularyFunctionalTestCase
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName


class TestSetup(PleiadesVocabularyFunctionalTestCase):

    def afterSetUp(self):
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPleiadesSettings)

    def test_vocabs(self):
        self.failIf(getattr(self.settings, 'name-accuracy', None) is None)
        self.failIf(getattr(self.settings, 'association-certainty', None) is None)
        self.failIf(getattr(self.settings, 'attestation-confidence', None) is None)
        self.failIf(getattr(self.settings, 'name-completeness', None) is None)
        self.failIf(getattr(self.settings, 'ancient-name-languages', None) is None)
        self.failIf(getattr(self.settings, 'name-types', None) is None)
