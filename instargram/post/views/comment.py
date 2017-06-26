from django.shortcuts import redirect, render, get_object_or_404

from ..forms.comment import CommentForm
from post.models import Post, Comment


def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post_pk = comment.post_id
    form = CommentForm(request.POST, instance=comment)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        form = CommentForm()
    context = {
        'comment_form': form,
    }
    return render(request, 'post/comment_modify.html', context)
