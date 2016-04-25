from zope.component import getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from five import grok

from plone.registry.interfaces import IRegistry

from pleiades.vocabularies.interfaces import IPleiadesSettings


def registry_vocabulary(field, value_filter=None):
    path = field.interface.__identifier__ + '.' + field.__name__

    def vocabulary_factory(context):
        registry = getUtility(IRegistry)
        values = registry.get(path, {})
        values = values.keys()
        values.sort()
        terms = []
        for value in values:
            terms.append(SimpleTerm(
                value=value,
                token=value.encode('raw_unicode_escape'),
                title=value,
                ))
        return SimpleVocabulary(terms)

    directlyProvides(vocabulary_factory, IVocabularyFactory)
    return vocabulary_factory


time_periods = IPleiadesSettings['time_periods']
vocabulary = registry_vocabulary(time_periods)
vocabulary_name = 'pleiades.vocabularies.time_periods'
grok.global_utility(vocabulary, name=vocabulary_name, direct=True)
