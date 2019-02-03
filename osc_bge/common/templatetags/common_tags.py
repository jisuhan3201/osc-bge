from django import template
register = template.Library()


@register.filter
def get_list(querydict, itemkey):

    return querydict.getlist(itemkey)
