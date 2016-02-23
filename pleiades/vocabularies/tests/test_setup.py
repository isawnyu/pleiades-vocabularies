from pleiades.vocabularies.tests.base import PleiadesVocabularyFunctionalTestCase
from Products.CMFCore.utils import getToolByName


class TestSetup(PleiadesVocabularyFunctionalTestCase):

    def afterSetUp(self):
        self.vocabs = getToolByName(self.portal, 'portal_vocabularies')
        self.uvocabs = self.portal['vocabularies']
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')

    def test_vocabs(self):
        self.failUnless('name-accuracy' in self.vocabs.keys())
        self.failUnless('association-certainty' in self.vocabs.keys())
        self.failUnless('place-types' in self.vocabs.keys())
        self.failUnless('attestation-confidence' in self.vocabs.keys())
        self.failUnless('time-periods' in self.vocabs.keys())
        self.failUnless('name-completeness' in self.vocabs.keys())
        self.failUnless('ancient-name-languages' in self.vocabs.keys())
        self.failUnless('name-types' in self.vocabs.keys())

    def test_uvocabs(self):
        self.failUnless('name-accuracy' in self.uvocabs.keys())
        self.failUnless('association-certainty' in self.uvocabs.keys())
        self.failUnless('place-types' in self.uvocabs.keys())
        self.failUnless('attestation-confidence' in self.uvocabs.keys())
        self.failUnless('time-periods' in self.uvocabs.keys())
        self.failUnless('name-completeness' in self.uvocabs.keys())
        self.failUnless('ancient-name-languages' in self.uvocabs.keys())
        self.failUnless('name-types' in self.uvocabs.keys())

    def test_vocab_data(self):
        v = self.vocabs['name-accuracy']
        t = v.getTarget()
        self.assertEquals(
            t.getVocabularyDict(all=True),
            {'accurate': 'accurate', 'false': 'false', 'inaccurate': 'inaccurate'})
        d = v.getVocabularyDict(v)
        self.assertEquals(
            d, {'accurate': 'accurate', 'false': 'false', 'inaccurate': 'inaccurate'})

    def test_namedvocab(self):
        from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
        nv = NamedVocabulary('name-accuracy')
        d = nv.getVocabularyDict(self.portal)
        self.assertEquals(d, {'accurate': 'accurate', 'false': 'false', 'inaccurate': 'inaccurate'})
