from pleiades.vocabularies.tests import base
from Testing import ZopeTestCase as ztc
import doctest
import unittest

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


class TestCase(base.PleiadesVocabularyFunctionalTestCase):
    pass


def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'user-terms.txt',
            package='pleiades.vocabularies.tests',
            test_class=TestCase,
            optionflags=optionflags
            ),
        ])
