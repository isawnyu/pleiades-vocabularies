from zope import schema
from zope.interface import Interface

from collective.z3cform.datagridfield.registry import DictRow


class IPeriodSchema(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')
    description = schema.TextLine(title=u'Description', required=False)
    lower_bound = schema.Int(title=u'Lower')
    upper_bound = schema.Int(title=u'Upper')
    same_as = schema.URI(title=u'Same As', required=False)
    hidden = schema.Bool(title=u'Hidden', default=False)


class IVocabTerm(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')


class IVocabTermExtended(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')
    description = schema.TextLine(title=u'Description', required=False)
    same_as = schema.URI(title=u'Same As', required=False)
    hidden = schema.Bool(title=u'Hidden', default=False)


class IZoteroWork(Interface):
    short_title = schema.TextLine(title=u'Short title')
    zotero_uri = schema.URI(title=u'Zotero URI')


class IPleiadesSettings(Interface):
    """Global Pleiades site specific settings"""

    time_periods = schema.List(
        title=u'Time Periods',
        value_type=DictRow(
            title=u'Period',
            schema=IPeriodSchema,
        )
    )

    place_types = schema.List(
        title=u'Place Types',
        value_type=DictRow(
            title=u'Place Type',
            schema=IVocabTermExtended,
        )
    )

    arch_remains = schema.List(
        title=u'Archaeological Remains',
        value_type=DictRow(
            title=u'Remains Entry',
            schema=IVocabTerm,
        )
    )

    location_types = schema.List(
        title=u'Location Types',
        value_type=DictRow(
            title=u'Location Entry',
            schema=IVocabTerm,
        )
    )

    relationship_types = schema.List(
        title=u'Relationship Types',
        value_type=DictRow(
            title=u'Relationship Entry',
            schema=IVocabTermExtended,
        )
    )

    association_certainty = schema.List(
        title=u'Association Certainty',
        value_type=DictRow(
            title=u'Association Certainty',
            schema=IVocabTermExtended,
        )
    )

    attestation_confidence = schema.List(
        title=u'Attestation Confidence',
        value_type=DictRow(
            title=u'Attestation Confidence',
            schema=IVocabTermExtended,
        )
    )

    ancient_name_languages = schema.List(
        title=u'Language and Script',
        value_type=DictRow(
            title=u'Language and Script',
            schema=IVocabTermExtended,
        )
    )

    name_types = schema.List(
        title=u'Name Types',
        value_type=DictRow(
            title=u'Name Types',
            schema=IVocabTermExtended,
        )
    )

    name_accuracy = schema.List(
        title=u'Name Accuracy',
        value_type=DictRow(
            title=u'Name Accuracy',
            schema=IVocabTermExtended,
        )
    )

    name_completeness = schema.List(
        title=u'Name Completeness',
        value_type=DictRow(
            title=u'Name Completeness',
            schema=IVocabTermExtended,
        )
    )

    default_works = schema.List(
        title=u"Default works",
        value_type=DictRow(
            title=u'Default work',
            schema=IZoteroWork,
        )
    )
