import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """
    ファイルパスからファイル名を取得するカスタムフィルタ
    """
    return os.path.basename(value)
