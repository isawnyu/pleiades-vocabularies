import unittest
from pleiades.vocabulary.tests.base import PleiadesVocabularyTestCase
from Products.CMFCore.utils import getToolByName


class TestSetup(PleiadesVocabularyTestCase):

    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
    
    def test_structure(self):
        self.failUnless('vocabulary' in self.portal.keys())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
