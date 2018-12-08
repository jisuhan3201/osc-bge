from django.template.defaulttags import register as default_register
from django import template
register = template.Library()

@default_register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def index(List, i):
    return List[int(i)]
