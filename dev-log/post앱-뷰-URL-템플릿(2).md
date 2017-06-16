### post_detail 뷰 구상하기
- Post 모델에 해당 데이터가 존재하면, 인자로 받은 pk와 동일한 값이 포함된 Row 데이터를 post 변수에 할당한다.
- 데이터가 존재하지 않으면, post/post_list.html 로 돌아간다.
- render() 를 통하여 post 의 값을 딕셔너리 형태로 post_detail.html 에 전달한다.

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

### post_detail URL 구상하기
- Post 모델로부터 불러온 pk 값을 매개로 정규표현식을 통해 post_detail URL 을 만든다.

```python
...
urlpatterns = [
  ...
  url(r'^(?P<post_pk>\d+)/$', view.post_detail, name='post_detail')
]
...
```

### 기본 골격이 되는 부모페이지 base.html
- templates 디렉토리 하위에 common 디렉토리 생성 후, base.html 을 생성한다.

[common/base.html]
```python
... html 구성하는 기본 태그들
<body>
  {% block content %}
  {% endblock %}
</body>
```
- base.html 을 상속 받을 페이지에 'extends'를 통해서 상속시킨다.

[post_list.html], [post_detail] 등 자식 페이지들
```python
{% extends 'common/base.html' %}
{% block content %}
  #... 깃 코드 참조
{% endblock %}
```

### post_list와 post_detail이 공통으로 사용할 페이지 post.html
- tempaltes 디렉토리 아래 include 디렉토리 생성 후, post.html 작성

[include/post.html]
```python
#... 템플릿 언어를 활용해서 작성, 깃 코트 참조
```

[post_list.html], [post_detail] 에 include
```python
...
{% include 'include/post.html' %}
```
- 'include'를 통해 post.html 을 포함시킨다.

> Git Code Address ヾ(๑ㆁᗜㆁ๑)ﾉ
- [post/veiws.py](https://github.com/bbungsang/Instargram-projects/blob/master/instargram/post/views.py)
- [post/urls.py](https://github.com/bbungsang/Instargram-projects/blob/master/instargram/post/urls.py)
- [templates](https://github.com/bbungsang/Instargram-projects/tree/master/instargram/templates) 
