from .widgets import AdminIconChooser
from wagtail.admin.edit_handlers import FieldPanel

class IconsChooserPanel(FieldPanel):
    def widget_overrides(self):
        return {
            self.field_name: AdminIconChooser(),
        }
