from zope.interface import Interface, implements
from zope.publisher.browser import BrowserView


class IVocabulariesIndex(Interface):
    pass


class VocabulariesIndex(BrowserView):
    implements(IVocabulariesIndex)
    

class IVocabularyView(Interface):
    pass


class VocabularyView(BrowserView):
    implements(IVocabularyView)


class VocabularyMacros(BrowserView):
    pass

