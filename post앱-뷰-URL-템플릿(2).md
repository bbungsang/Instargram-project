```python
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
```
