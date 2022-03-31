from django import template

register = template.Library()


@register.filter
def ext(path_name):
    import os
    name, extention = os.path.splitext(path_name)
    if extention[1:]:
        return extention[1:]
    else:
        return ''
