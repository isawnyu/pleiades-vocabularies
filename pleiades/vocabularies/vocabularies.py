from binascii import b2a_qp

from zope.component import getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from plone.registry.interfaces import IRegistry

from pleiades.vocabularies.interfaces import IPleiadesSettings


def registry_vocabulary(field, value_filter=None):

    def vocabulary_factory(context):
        values = get_vocabulary(field.__name__)
        terms = []
        for value in values:
            terms.append(SimpleTerm(
                value=value['id'],
                token=b2a_qp(value['id'].encode('utf-8')),
                title=value['title'],
                ))
        return SimpleVocabulary(terms)

    directlyProvides(vocabulary_factory, IVocabularyFactory)
    return vocabulary_factory


time_periods = IPleiadesSettings['time_periods']
time_periods_vocabulary = registry_vocabulary(time_periods)

arch_remains = IPleiadesSettings['arch_remains']
arch_remains_vocabulary = registry_vocabulary(arch_remains)


def get_vocabulary(name):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPleiadesSettings)
    vocabulary = getattr(settings, name)
    if vocabulary is None:
        return []
    if name == 'time_periods':
        return sorted(vocabulary, key=lambda k: k['lower_bound'])
    else:
        return vocabulary
