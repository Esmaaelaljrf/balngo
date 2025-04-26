from django.contrib.auth import get_user_model
from django import template
#from django.utils.html import escape # تستخدم لإخراج وتمييز جزء من الكود وهنا قمنا بإخراج المدخلات من قبل المستخدم
#from django.utils.safestring import mark_safe#لاخبار جانغو ان هذا الكود امن ويمكن الوثوق به وعرضه

from django.utils.html import format_html #we this work like (escape&mark_safe) Together 

register = template.Library()
user_model = get_user_model()# it checkes  the model that we use it, "here have to be Post".

@register.filter
def author_details(author, current_user):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""
    
    if author == current_user:
        return format_html("<strong>me</strong>")

    
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)
    #here we render the code safeitly