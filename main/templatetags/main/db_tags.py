from django import template
from ... import models

register = template.Library()


@register.simple_tag(takes_context=True)
def key(context):
    pass

