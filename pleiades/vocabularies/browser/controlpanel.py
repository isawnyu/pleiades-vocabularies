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

    def datagridUpdateWidgets(self, subform, widgets, widget):
        widgets['id'].size = 20
        widgets['lower_bound'].size = 5
        widgets['upper_bound'].size = 5
        widgets['title'].size = 20
        widgets['description'].size = 30
        widgets['same_as'].size = 20


class PleiadesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PleiadesSettingsEditForm
