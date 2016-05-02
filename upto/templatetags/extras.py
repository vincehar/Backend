from django import template

register = template.Library()

@register.filter
def wishNumber(wishes):
    return len(wishes)