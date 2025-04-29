from django.contrib.auth import get_user_model
from django import template
from blog.models import Post
from django.utils.html import format_html #we this work like (escape&mark_safe) Together 

#from django.utils.html import escape # تستخدم لإخراج وتمييز جزء من الكود وهنا قمنا بإخراج المدخلات من قبل المستخدم
#from django.utils.safestring import mark_safe#لاخبار جانغو ان هذا الكود امن ويمكن الوثوق به وعرضه

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
#------------------------------------

#we use simple_tag to write a little words of html code
#Here write our tags then have to register them, finally we can use them in html's files
@register.simple_tag 
def row(extra_classes=""): # using this function we will use {% row %} just without the full code of html to use row class
    return format_html('<div class="row {}">', extra_classes)#extra_classes: it make us to use the argumants with row class in the html file

@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")
#----------------------


@register.inclusion_tag("blog/post-list.html")#didn't work(No wrong message) +post-list file+ the part of it on post-deail file
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}