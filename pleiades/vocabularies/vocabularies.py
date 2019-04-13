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

place_types = IPleiadesSettings['place_types']
place_types_vocabulary = registry_vocabulary(place_types)

arch_remains = IPleiadesSettings['arch_remains']
arch_remains_vocabulary = registry_vocabulary(arch_remains)

location_types = IPleiadesSettings['location_types']
location_types_vocabulary = registry_vocabulary(location_types)

relationship_types = IPleiadesSettings['relationship_types']
relationship_types_vocabulary = registry_vocabulary(relationship_types)

association_certainty = IPleiadesSettings['association_certainty']
association_certainty_vocabulary = registry_vocabulary(association_certainty)

attestation_confidence = IPleiadesSettings['attestation_confidence']
attestation_confidence_vocabulary = registry_vocabulary(attestation_confidence)

ancient_name_languages = IPleiadesSettings['ancient_name_languages']
ancient_name_languages_vocabulary = registry_vocabulary(ancient_name_languages)

name_types = IPleiadesSettings['name_types']
name_types_vocabulary = registry_vocabulary(name_types)

name_accuracy = IPleiadesSettings['name_accuracy']
name_accuracy_vocabulary = registry_vocabulary(name_accuracy)

name_completeness = IPleiadesSettings['name_completeness']
name_completeness_vocabulary = registry_vocabulary(name_completeness)


def get_vocabulary(name):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPleiadesSettings)
    vocabulary = getattr(settings, name)
    if vocabulary is None:
        return []
    if name == 'time_periods':
        return sorted(vocabulary, key=lambda k: k['lower_bound'])
    elif name in ('place_types', 'ancient_name_languages',
                  'attestation_confidence', 'name_types',
                  'name_accuracy', 'name_completeness'):
        return sorted(vocabulary, key=lambda k: k['title'])
    else:
        return vocabulary
