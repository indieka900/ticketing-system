import os
from django import template

register = template.Library()

@register.filter(name='get_file_type')
def get_file_type(filename):
    ext = os.path.splitext(filename)[-1].lower()
    if ext in {".jpg", ".jpeg", ".png"}:
        return "Image"
    elif ext in {".docx", ".doc"}:
        return "Word Document"
    elif ext == ".pdf":
        return "PDF"
    else:
        return "Unknown"
register.filter(name='get_file_type')