from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

class EditInlineButton:
    list_display_links = ('edit_button',)

    def get_list_display(self, request):
        # add show button in all list_displays
        _super = super().get_list_display(request)
        
        list_display = []
        list_display.extend(
            ["pk", "is_active"] +
            list(_super) +
            ["created_time", "updated_time", 'edit_button']
        )
        return list_display

    def edit_button(self, obj):
        return mark_safe(f'<input type="button" class="edit_button" value={_("edit")} />')

    edit_button.short_description = _("edit")
    edit_button.allow_tags = True