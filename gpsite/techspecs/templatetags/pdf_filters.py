from django import template
from django.conf import settings
import os

register = template.Library()
@register.filter
def get64(url):
    murl = settings.MEDIA_URL
    mroot = settings.MEDIA_ROOT
    if url.startswith(murl):
        path = os.path.join(mroot, url.replace(murl, ''))
        return path
    return url