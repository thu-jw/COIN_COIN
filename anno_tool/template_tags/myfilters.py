#!/usr/bin/env python3
from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
# vim: ts=4 sw=4 sts=4 expandtab
