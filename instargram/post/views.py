from django.shortcuts import render, redirect
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(
        request,
        'post/post_list.html',
        context,
    )


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoseNotExist:
        return redirect('post:post_list')

    return render(
        request,
        'post/post_detail.html',
        {
            'post': post,
        },
    )