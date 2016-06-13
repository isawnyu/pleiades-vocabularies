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
        self.fields['time_periods'].widgetFactory = DataGridFieldFactory
        self.fields['time_periods'].allow_insert = True
        self.fields['arch_remains'].widgetFactory = DataGridFieldFactory
        self.fields['arch_remains'].allow_insert = True

    def datagridUpdateWidgets(self, subform, widgets, widget):
        if 'id' in widgets['id']:
            widgets['id'].size = 20
        if 'lower_bound' in widgets:
            widgets['lower_bound'].size = 5
        if 'upper_bound' in widgets['upper_bound']:
            widgets['upper_bound'].size = 5
        if 'title' in widgets['title']:
            widgets['title'].size = 20
        if 'description' in widgets['description']:
            widgets['description'].size = 30
        if 'same_as' in widgets['same_as']:
            widgets['same_as'].size = 20


class PleiadesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PleiadesSettingsEditForm
