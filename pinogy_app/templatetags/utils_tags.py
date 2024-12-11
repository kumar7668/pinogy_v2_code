from django import template

register = template.Library()


@register.filter
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

    return dict_data