from AccessControl import ClassSecurityInfo
from ExtensionClass import Base
from Products.Archetypes.Widget import InAndOutWidget
from Products.Archetypes.Widget import SelectionWidget
from .vocabularies import get_vocabulary


class FilteredWidgetMixin(Base):

    security = ClassSecurityInfo()

    @security.public
    def hidden_terms(self, field):
        vocab_name = getattr(field, 'vocabulary_factory').split('.')[-1]
        terms = []
        for term in get_vocabulary(vocab_name):
            if term['hidden']:
                terms.append(term['id'])
        return terms


class FilteredSelectionWidget(FilteredWidgetMixin, SelectionWidget):
    """A selection widget that filters out hidden options unless selected"""
    _properties = SelectionWidget._properties.copy()
    _properties.update({
        'macro': "filtered_selection",
        })


class FilteredInAndOutWidget(FilteredWidgetMixin, InAndOutWidget):
    """A selection widget that filters out hidden options unless selected"""
    _properties = InAndOutWidget._properties.copy()
    _properties.update({
        'macro': "filtered_inandout",
        })
