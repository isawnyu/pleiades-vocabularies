from zope import schema
from zope.interface import Interface

from collective.z3cform.datagridfield.registry import DictRow


class IPeriodSchema(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')
    description = schema.TextLine(title=u'Description')
    lower_bound = schema.Int(title=u'Lower')
    upper_bound = schema.Int(title=u'Upper')
    same_as = schema.URI(title=u'Same As', required=False)
    hidden = schema.Bool(title=u'Hidden', default=False)


class IPleiadesSettings(Interface):
    """Global Pleiades site specific settings"""
    time_periods = schema.List(
        title=u'Time Periods',
        value_type=DictRow(title=u'Period',
                           schema=IPeriodSchema)
        )
