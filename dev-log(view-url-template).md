## 첫 뷰, 첫 URL, 첫 템플릿 설정하기
### 첫 뷰 구상하기
- Post 모델의 데이터를 전부 불러와서 리스트 형태로 화면에 순차적으로 출력

[post/views.py]
```python
from django.shortcuts import render

# 1. Post 모델을 호출할 것이므로 models.py의 Post를 임포트한다.
from .models import Post

# 2. url로 부터 전달되어 실행할 함수를 작성한다.
def post_list(request):

  # 3. Post 모델의 모든 데이터를 이터레이터 형태로 받아와서 posts 변수에 할당
  posts = Post.objects.all()

  # 4. 함수 내부에서 정의된 값을 템플릿에 넘겨주기 위해 딕셔너리 형태의 context 정의.
  context = {
    'posts': posts
  }

  # 5. render() 의 첫번째 인자: 외부로 부터 요청된 값인 request, 두번째 인자: 값을 받아서 보여줄 템플릿, 세번째 인자: context
  return render(
    request,
    'post/post_list.html',
    context
  )
```

### 첫 URL 구상하기
- 등록한 어플리케이션의 뷰를 사용하기 위해서는 프로젝트 urls.py 에 include 시켜줘야한다. 이 경우 어플리케이션을 생성할 때마다 1번만 해주면 된다.

[config/urls.py]
```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/', include('post.urls')),
]
```
[post/urls.py]
```python
from django.conf.urls import url
from . import views

# 뷰의 key로 앱 이름 'post'를 지정해준다.
app-name='post'
urlpatterns = [

  # /post/의 URL로 post_list라는 이름의 뷰가 할당되고, 뷰를 식별하기 위해 이름을 붙임
  url(r'^$', views.post_list, name=post_list),
]
```

### 첫 템플릿 구상하기
- 여러 어플리케이션이 공통으로 템플릿을 이용할 수 있도록 루트 폴더 아래 템플릿 폴더를 지정할 것이다. 이를 위해서 우선 settings.py에서 템플릿을 인식할 폴더의 위치를 아래와 같이 명시해줘야 한다.

[config/settins.py]
```python
...
# root-dir/templates
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
  {
    #...
    'DIRS': [
        TEMPLATE_DIR,
    ],
    #...
  }
  #...
```
- 이렇게 하고 /post/ 의 URL로 접속하면 화면이 잘 뜬다. 하지만 이미지를 못 불러온다. 이미지를 불러올 수 있도록 몇 가지 설정해야 할 부분이 있다.


1. Pillow 설치하기(Ubuntu 기준)

  - Pillow를 설치하기 전에 설치해야 할 것
  - $sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
- 사전 설치작업 완료 후, Pillow 설치하기
  - $ pip install Pillow

2. 루트 폴더 아래 'media' 폴더 생성 후, settings.py에서 경로 설정과 urls.py에 media의 파일을 읽어올 수 있도록 아래와 같이 지정해준다.

[config/settings.py]
```python
...
# root-dir/media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
...
```
[config/urls.py]
```python
...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- 이미지 출력 완료!
