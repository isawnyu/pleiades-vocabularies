from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('ATVocabularyManager')

@onsetup
def setup_pleiades_vocabularies():
    """Set up the additional products required for the Pleiades site policy.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """

    # Load the ZCML configuration for the optilux.policy package.
    
    fiveconfigure.debug_mode = True
    import pleiades.vocabularies
    zcml.load_config('configure.zcml', pleiades.vocabularies)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('pleiades.vocabularies')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the Pleiades package. Then, we let 
# PloneTestCase set up this product on installation.

setup_pleiades_vocabularies()
ptc.setupPloneSite(products=['pleiades.vocabularies'])

class PleiadesVocabularyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """


class PleiadesVocabularyFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

    def afterSetUp(self):
        try:
            self.folder.invokeFactory('Folder', id='vocabularies')
            # self.folder['vocabularies'].invokeFactory('PleiadesVocabulary', id='quality')
            # self.folder['vocabularies']['quality'].invokeFactory('PleiadesVocabularyTerm', id='good', key='good', value='Good')
            # 
        except:
            pass
