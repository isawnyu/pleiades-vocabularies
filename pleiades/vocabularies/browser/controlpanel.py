from plone.app.registry.browser import controlpanel
from collective.z3cform.datagridfield import DataGridFieldFactory

from ..interfaces import IPleiadesSettings


class PleiadesSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPleiadesSettings
    label = u"Pleiades Site Settings"
    description = u""
    enableCSRFProtection = True

    def updateFields(self):
        super(PleiadesSettingsEditForm, self).updateFields()
        for field in (
                'arch_remains', 'location_types', 'place_types',
                'relationship_types', 'time_periods', 'association_certainty',
                'ancient_name_languages', 'attestation_confidence',
                'name_types', 'name_accuracy', 'name_completeness',
                'default_works'
                ):
            self.fields[field].widgetFactory = DataGridFieldFactory
            self.fields[field].allow_insert = True

    def datagridUpdateWidgets(self, subform, widgets, widget):
        if 'id' in widgets.keys():
            widgets['id'].size = 20
        if 'lower_bound' in widgets.keys():
            widgets['lower_bound'].size = 5
        if 'upper_bound' in widgets.keys():
            widgets['upper_bound'].size = 5
        if 'title' in widgets.keys():
            widgets['title'].size = 20
        if 'description' in widgets.keys():
            widgets['description'].size = 30
        if 'same_as' in widgets.keys():
            widgets['same_as'].size = 20


class PleiadesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PleiadesSettingsEditForm
