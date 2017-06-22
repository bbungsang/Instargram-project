from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

from ..models import Post, Comment
from ..forms import PostForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


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

        # redirect('post:post_list') 과 같은 역할을 한다.
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    # 템플릿을 반환하는 방법은 간단하게 render() 를 사용하는 방식과, template_get() 을 사용하는 약간 복잡한 방법이 있다.
    ### 1. render()
    '''
    return render(
        request,
        'post/post_detail.html',
        {
            'post': post,
        },
    )
    '''

    ### 2. template_get()
    '''
    template_get() 에 의해 반환된 템플릿 객체는 render(context=None, request=None) 를 제공해야한다.
    context 는 반드시 딕셔너리 형태여야 한다.
    render() 를 사용해서 template 을 string 으로 변환되면 HttpResponse 형태로 반환한다.
    '''

    # get_template() 를 통해 post/post_detail.html 템플릿을 로드한다.
    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }

    # 템플릿 객체를 render() 를 통해서 string 으로 변환하고 render_to_string 변수에 할당한다.
    render_to_string = template.render(context=context, request=request)
    return HttpResponse(render_to_string)


def post_create(request):
    if request.method == 'POST':

        '''
        # 1) PostForm 을 쓰지 않았을 경우,
        user = User.objects.first()

        post = Post.objects.create(
            author=user,
            photo=request.FILES['photo']
        )

        # POST 요청으로 받은 comment 인자의 value 를 comment_string 변수에 할당
        # value 가 없을 경우(빈 문자열이거나 None), False 로 평가된다.
        comment_string = request.POST.get('comment', '')

        # if 문을 통해서 comment 의 존재 여부를 판단
        if comment_string:
            # 1-1. Comment 모델을 Post 모델에서 역참조하여 데이터를 처리한다.
            post.comment_set.create(
                author=user,
                content=comment_string,
            )

            # 1-2. 바로 Comment 모델에 접근하여 데이터를 처리한다.
            Comment.objects.create(
                post=post,
                author=user,
                content=comment_string,
            )
        '''

        '''
        2) PostForm 을 사용할 경우,
            1. 폼 위젯을 생성한다. [forms/post.py]
            2. 폼으로부터 얻어온 데이터를 form 변수에 할당한다. [views/post.py]
            3. form 변수를 활용하여 폼 유효성 메서드를 실행한다. [views/post.py]
            4. form 변수를 통해 save(author='request.user') -> commit=False 를 실행하고, 반환된 인스터스를 post 변수에 할당한다. [views/post.py]
            5. save() 메서드를 작성한다. [forms/post.py]
        '''
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_modify(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = PostForm(data=request.POST, files=request.FILES, instance=post)
    if request.method == "POST":
        form.save()
        return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'post/post_create.html', context)