from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.all()

    lorempixel_categories = (
        "abstract", "animals", "business", "cats", "city", "food", "night",
        "life", "fashion", "people", "nature", "sports", "technics", "transport",
    )

    return render(request, 'blog/index.html', {
        'post_list': post_list,
        'lorempixel_categories': lorempixel_categories,
    })


def detail(request, pk):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post
    })


@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pk)
            comment.save()
            return redirect('blog.views.detail', pk)
    else:
        form = CommentForm()

    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog.views.detail', post_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/form.html', {
        'form': form,
    })
