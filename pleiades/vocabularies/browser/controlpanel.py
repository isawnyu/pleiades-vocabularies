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
        self.fields['relationship_types'].widgetFactory = DataGridFieldFactory
        self.fields['relationship_types'].allow_insert = True

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
