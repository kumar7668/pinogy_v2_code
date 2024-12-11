from django.forms import widgets
from cms.forms.widgets import PageSmartLinkWidget

FORM_INPUT_TYPE = ['text', 'number']

class BootstrapMixin:
    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css",
                "https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css",
                "https://fonts.googleapis.com/css?family=Open+Sans:400,600,300",
                "css/banner-form.css",
                "css/custom-admin-form.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js",
            "https://code.jquery.com/jquery-3.6.3.min.js",
            "https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js",
            "https://cdn.ckeditor.com/ckeditor5/41.0.0/super-build/ckeditor.js",
            "js/color_palette_widget.js",
            # "js/ckeditor_widget.js",
        )


class TextBoxWidget(BootstrapMixin, widgets.TextInput):
    """
    Display Textbox with color icon
    attrs:
        - is_color_box_display : bool = True
        - input_type: str = text
        - placeholder: str
        - label: str
        - class: str
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/text_box.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        if context["widget"]["attrs"].get("is_color_box_display") is None:
            context["widget"]["attrs"]["is_color_box_display"] = False
            
        if context["widget"]["attrs"].get("input_type") is None or context["widget"]["attrs"].get("input_type") not in FORM_INPUT_TYPE:
            context["widget"]["attrs"]["input_type"] = 'text'

        return context


class ColorPalette(BootstrapMixin, widgets.Widget):
    """
    Display black, white, primary, secondary, and custom picker
    attrs:
        - label : str
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/color_palette.html"


class CustomButton(BootstrapMixin, widgets.Widget):
    """
    Display black, white, primary, secondary, and custom picker
    attrs:
        - label : str
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/custom_button.html"

class Image(BootstrapMixin, widgets.Widget):
    """
    Display black, white, primary, secondary, and custom picker
    attrs:
        - label : str
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/image.html"

class CustomCheckBox(BootstrapMixin, widgets.CheckboxSelectMultiple):
    """
    Display checkbox fields
    attrs:
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/custom_checkbox.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # adding checkbox elements in context
        checkbox_elements = [elem[1][0] for elem in context['widget']['optgroups']]
        context["checkbox_elements"] = checkbox_elements

        return context

class CustomRadioSelect(BootstrapMixin, widgets.RadioSelect):
    """
    Display radioselect fields
    attrs:
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
        - horizontal_layout : bool
    """

    template_name = "custom_design/forms/widgets/custom_radio_select.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # adding radio elements in context
        radio_elements = []
        for elem in context['widget']['optgroups']:
            radio_elements.append(elem[1][0])
        context["radio_elements"] = radio_elements

        return context

class CustomBoolean(BootstrapMixin, widgets.CheckboxInput):
    """
    Display Custom checkbox for boolean
    attrs:
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
        - label : str
    """

    template_name = "custom_design/forms/widgets/custom_boolean.html"

class LinkWidget(BootstrapMixin, PageSmartLinkWidget):
    """
    Display Textbox with color icon
    attrs:
        - placeholder: str
        - label: str
        - class: str
        - section_heading : str
        - section_heading_desc : str
        - section_divider : bool
    """

    template_name = "custom_design/forms/widgets/link_widget.html"

    
    def __init__(self, attrs=None, ajax_view=None):
        self.language = "en"
        super().__init__(attrs, ajax_view)

class CKEditorTextboxWidget(BootstrapMixin, widgets.Widget):
    """
    Display Textbox with color icon
    attrs:
        - label : str
        - class : str
        - placeholder: str
        - section_heading : str
        - section_heading_desc : str
        - toolbars : list (str)
        - fontFamily : list (str)
        - fontSize : list (number)
        - heading : list (str)
        - paragraph : bool
        - section_divider : bool
    """
    """
    Note : fontSize list should be like [1,3,10] and other in ["Aerial","san-serif"]
    """
    template_name = "custom_design/forms/widgets/ckeditortextarea.html"

