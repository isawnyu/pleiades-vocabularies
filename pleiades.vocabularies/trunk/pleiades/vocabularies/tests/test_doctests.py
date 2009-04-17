import unittest
import doctest
from Testing import ZopeTestCase as ztc

from pleiades.vocabularies.tests import base
optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def test_suite():
    return unittest.TestSuite([
        # ztc.FunctionalDocFileSuite(
        #     'vocab-views.txt',
        #     package='pleiades.vocabularies.tests',
        #     test_class=base.PleiadesVocabularyFunctionalTestCase,
        #     optionflags=optionflags
        #     )
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
