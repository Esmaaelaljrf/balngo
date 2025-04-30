from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from blog.forms import CommentForm#is a form takes the request's contents

# Create your views here.
def index(request):
    return render(request, "blog/index.html")

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:#check if the current is logged(has an accunt)
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)#here we put the data in a form without save it on the database
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)#here we reload the page using(redirect ) to render new commit
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )