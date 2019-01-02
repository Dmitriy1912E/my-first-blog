from django import template

register = template.Library()


@register.filter
def multiply(value, index):
    return value * index
