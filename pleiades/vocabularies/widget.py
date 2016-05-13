from AccessControl import ClassSecurityInfo

from Products.Archetypes.Widget import TypesWidget

from .vocabularies import get_vocabulary


class TimePeriodSelectionWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'format': "flex",  # possible values: flex, select, radio
        'macro': "time_period_selection",
        'blurrable': True,
        })

    security = ClassSecurityInfo()

    security.declarePublic('render_own_label')
    def render_own_label(self):
        return True

    security.declarePublic('render_own_label')
    def show_term(self, item):
        time_periods = get_vocabulary('time_periods')
        for term in time_periods:
            if term['id'] == item and not term['hidden']:
                return True
        return False
