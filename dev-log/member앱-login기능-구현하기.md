# 로그인 기능 구현하기
폼 -> 뷰 -> URL -> 템플릿 순서로 구현하려고 한다.

> 고려해야할 부분
  1. 아이디와 비밀번호를 입력할 폼 작성
  2. POST 요청이 아닐 경우, 빈 로그인 폼을 받아서 로그인 페이지에 넘긴다.
  3. 사용자가 폼을 입력하지 않으면, 입력 요청 메세지를 띄우며 다음 페이지로 이동을 막는다.
  4. 입력한 아이디와 비밀번호가 데이터베이스의 데이터와 일치하지 않을 경우, 에러 메세지를 뿜뿜하며 다음 페이지로 이동을 막고, 일치할 경우, 장고 로그인 메서드를 실행하고 post_list 페이지로 이동.
  5. 이미 로그인한 상태에서 로그인 페이지로 이동한 것이라면 post_list 페이지로 되돌린다.

### 1. 장고 폼에서 위젯을 생성하고, 데이터 유효성 및 하자 여부 검사하기
- LoginForm, SignupForm과 앞으로 더 필요할 수 있는 폼들을 파이썬 패키지를 생성하여 하위 항목으로 둔다. 왜? 하나의 파일에 모든 폼 클래스를 작성하면, 코드가 길어져서 보기에 불편함을 겪을 수 있기 때문이다.
- member 앱 디렉토리에 forms 패키지를 생성하고 login.py를 생성하여 아래와 같이 작성한다.

[forms/login.py] : 폼 위젯 만들기
```python
from django import forms

class LoginForm(forms.Form):

  # 문자열을 받는 폼 필드에 최대 길이 30자, 문자열을 받는 위젯의 속성을 포함하여 username 에 할당
  # 즉, username 이 곧 하나의 필드가 된다.
  username = forms.CharField(
    max_length=30,
    widget=forms.TextInput(
      attrs={
        'placeholder': '아이디를 입력해주세요.'
      }
    )
  ) # 이 괄호 끝에 튜플이나 딕셔너리처럼 습관적으로 ','을 넣었었는데, 그 뒤 password 필드를 무시하게 되는 일이 발생했었다.

  # username 과 같이 입력 받을 password 필드 정의, 위젯의 경우, 패스워드는 문자열이 드러나면 곤란하기 때문에 forms.PasswordInput() 을 통해 문자열을 가려준다.
  password = forms.CharField(
      widget=forms.PasswordInput(
          attrs={
              'placeholder': '비밀번호를 입력해주세요.'
          }
      )
    )
```

#### 장고가 제공하는 유효성 검사기
- clean() 메서드는 단일 인수를 사용하여 잘못된 입력에 대해 ValidationError를 발생시키는 간단한 함수이다.
- 일반적으로 `is_valid()` 를 호출할 때 실행되고, `cleaned_data` 에 딕셔너리 { 'html-form-name': 'html-form-value' } 의 형태로 할당된다.
- 양식을 처리하면서 세 가지 유형 to_python(), validate(), run_validators() 을 순차적으로 실행한다.
- 처리 중인 데이터에 문제가 있으면 ValidationError 생성자에 관련 정보를 전달하여 클리닝 메서드가 ValidationError 를 발생시킨다.
- ValidationError 가 발생하지 않으면 정리된 데이터를 파이썬 객체로 반환해야 한다.

- **clean() 메서드**
  - to_python(), validate(), run_validators() 를 올바른 순서로 실행하고 오류 전파
  - ValidationError를 발생시키는 메서드가 있으면 유효성 검사가 중지되고 해당 오류가 발생, 깨끗한 데이터를 반환한 다음 폼의 cleaned_data 사전에 삽입
  - self.cleaned_data에서 필드 값을 찾고 이 시점에 파이썬 객체가 된다.

- **authenticate() 메서드**
  - 자격 증명이 유효한 경우, User 객체를 반환, 유효하지 않으면 None을 반환한다.
  - request 는 authenticate() 를 통과한 옵션 HttpRequest 다.

- authenticate() 를 통해 인증에 성공하면, cleaned_data 에 'user' 를 키값으로 User 객체를 할당한다.

[forms/login.py] : 데이터 유효성 및 하자 여부 검사하기
```python
#...
from django.contrib.auth import authenticate

#...
def clean(self):

    # is_valid() 가 실행되면서 사용자로 부터 폼에서 입력 받은 {'username': '사용자가 입력한 값', 'password': '사용자가 입력한 값'}이 cleaned_data 사전에 삽입될 것이다.
    # cleaned_data 사전으로 부터 username 과 password key 의 value 를 각각의 변수에 할당한다.  
    username = self.cleaned_data.get("username")
    password = self.cleaned_data.get("password")

    # value 가 유효하면 User 객체를 user 에 할당하고 유효하지 않으면 None 이 할당된다.
    user = authenticate(
        username=username,
        password=password,
    )

    # None 이 아니면(무효하지 않으면), cleaned_data 사전에 'user' 를 key 로 User 객체를 value 로 삽입한다.
    if user is not None:
        self.cleaned_data['user'] = user
    else:
        raise forms.ValidationError(
            'Login credentials not valid!'
        )

    # {'username': '사용자가 입력한 값', 'password': '사용자가 입력한 값', 'user': User 객체} 를 반환한다.    
    return self.cleaned_data
```

### 2. POST 요청이 아닐 경우, 빈 로그인 폼을 받아서 로그인 페이지로 넘기기
- 이 부분은 뷰가 처리한다.

[member/views.py] 에서 로그인을 위해 사용된 모듈
```python
from django.shortcuts import render, redirect
from member.forms.login import LoginForm
from django.contrib.auth import login as django_login, logout as django_logout,
```

[member/views.py]
```python
def login(request):
  if request.method == 'POST':
    pass
  else:
    form = LoginForm()
    context = {
      'form': form
    }
    return render(request, 'member/login.html', context)
```

### 3. 사용자가 폼을 입력하지 않으면, 입력 요청 메세지를 띄우며 다음 페이지 이동 막기
- 이 부분은 장고에서 알아서 해준다. 친절한 장고씨♡


### 4. 입력한 아이디와 비밀번호가 데이터베이스 데이터와 일치하지 않으면, 에러 메세지 뿜뿜! 하지만 일치하면, 로그인 하기
- 뷰에서 is_valid() 가 실행되면서 폼의 authenticate() 를 통해 데이터가 일치하면 User 객체를, 데이터가 없거나 일치하지 않으면 None 을 반환한다.
- None 일 경우 'Login credentials not valid!' 메세지를 띄우며 에러를 일으킨다.

[member/views.py]
```python
def login(request):
  if request.method == 'POST':
    form = LoginForm(data=request.post)

    if form.is_valid():

      # User 객체를 얻어서
      user = forms.cleaned_data['user']

      # 장고 로그인 메서드의 인자로 전달하여 로그인을 실행한다.
      django_login(request, user)
      return redirect('post:post_list')
    #...
```

### 5. 이미 로그인한 상태에서 로그인 페이지로 이동한 것이라면 post_list 페이지로 튕겨내기
```python
def login(request):
  form = forms.LoginForm(data=request.post)
  if form.is_valid():
    #...
  else:
    if request.user.is_authenticated():
      return redirect('post:post_list')
    #...
```
