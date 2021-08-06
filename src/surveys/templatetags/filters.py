from django import template
import hashlib

register = template.Library()

@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(str(value).encode()).hexdigest()