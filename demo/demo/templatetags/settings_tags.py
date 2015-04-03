# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.simple_tag
def get_title():
    return u"Автоматизированная информационная система кинотеатра"