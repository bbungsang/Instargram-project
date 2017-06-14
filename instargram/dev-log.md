#### 0. 어플리케이션 'post'를 생성하고, settings.py에 등록

#### 1. 모델 설계하기
- [Click!](https://github.com/bbungsang/Instargram-projects/blob/master/database-structure.pdf)

```python
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=36)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User)
    photo = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    like_user = models.ManyToManyField(
        User,
        through='PostLike',
    )


class PostLike(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_ad = models.DateTimeField(auto_now=True)

    like_user = models.ManyToManyField(
        User,
        through='CommentLike',
    )


class CommentLike(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    pass
```

#### 2. 설계한 모델과 필드를 작성하고 마이그레이션을 시도
- 아래와 같은 에러 발생

```text
'Post.author' clashes with reverse accessor for 'Post.like_user'
'Post.like_user' clashes with reverse accessor for 'Post.author'
'Comment.author' clashes with reverse accessor for 'Comment.like_user'
'Comment.like_user' clashes with reverse accessor for 'Comment.author'
```
- 이와 같은 에러는 지극히 개인적으로 해석한 바, Post/Comment 모델이 User 모델에 ForeignKey 와 ManyToMany 를 걸고 있고, 이로써 Post/Comment 모델과 User 모델에 생성된 reverse relation 에 FK에 대한 post_set/comment_set 속성, MTM에 대한 post_set/comment_set 속성이 각각 생성될 것이다. 즉, reverse relation 에서 중복된 속성명에 대한 충돌이 일어난 것.
- 따라서 둘 중 하나에 post_set/comment_set의 이름을 바꿔줘야한다. MTM을 건 각각의 like_user에 related_name을 줌으로써 이 충돌을 방지하려고 한다.

```python
#...

class Post(models.Model):
    author = models.ForeignKey(User)
    photo = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    like_user = models.ManyToManyField(
        User,
        through='PostLike',
        related_name='like_posts',
    )

#...

class Comment(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_ad = models.DateTimeField(auto_now=True)

    like_user = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='like_comments',
    )

#...
```
- 마이그레이션 에러를 극복했다!
- [Click!](https://github.com/bbungsang/Instargram-projects/blob/master/clash-error.pdf)

### 3. POST에 COMMENT를 추가할 수 있는 함수 구현
- 보통 처음에 함수 인스턴스까지 생각하고 애초에 모델에 적용했어야 했던게 맞는건지, 하다가 필요한 기능이 생기면 그 때 적용해도 되는건지 아직은 감이 안 잡히지만,
- 댓글 추가와 관련된 데이터를 가져올 수 있는 함수를 모델 첫 번째 마이그레이션을 마친 후 구현해본다.
- 한 POST에 댓글을 추가하는 방식이므로 POST모델에서 COMMENT모델을 역참조하여 해당 데이터를 가져올 수 있도록 한다.

```python
def add_comment(self, user, content):
    return self.post_set.create(author=user, content=content)
```
- 외부에서 user값과 content값을 받아서 COMMENT모델에 해당 데이터를 생성한다.

### 좋아요 개수를 세는 인스턴스를 프로퍼티로 표현
- 그 전에 프로퍼티의 개념이 잘 안서서 개념을 우선 정리해보겠다.

```python
class Monster():
    angelmon = '엔젤몬'

    def __init__(self, name):
        self.name = name

    def digimon(self,):
        return '{}은 디지몬입니다.'.format(
            self.name,
        )

>>> monster = Monster('파닥몬')
>>> monster.digimon()
# out : '파닥몬은 디지몬입니다.'

>>> monster.name
# out : '파닥몬'

>>> monster.name = '아구몬'
>>> monster.name
# out : '아구몬'
```
- 위와 같이 객체를 monster 변수에 할당하고 해당 객체가 갖고 있는 속성을 이용해서 바로 접근과 변경이 가능하다.
- 파이썬은 다른 객체 지향 언어와 달리 private, protected 개념이 구체적으로 없는 것으로 알고 있다.
- 접근 제한에 대한 개념이 뚜렷한 언어의 경우, getter와 setter를 통해 데이터에 접근하고, 변경이나 삭제를 할 수 있다.
- 하지만 파이썬은 그렇지 않은데 왜 굳이 property를 사용하는지 이해가 안됐다. 알아본 결과,
- 첫째, 추후 추가적인 무엇인가 필요한 경우, property에 추가하면 기존 코드가 손상되지 않는다.
- 둘째, 데이터 바인딩하기 좋다.

```python
class Monster():
    angelmon = '엔젤몬'

    def __init__(self, name):
        self.name = name

    def digimon(self):
        return '{}은 디지몬입니다.'.format(
            self.name,
        )

    @property
    def name(self):
        return '{}은 진화하면 {}이 됩니다.'.format(
            self.name,
            angelmon
        )

>>> monster = Monster('파닥몬')
>>> monster.digimon()
# out : can't set attribute
```
- name을 프로퍼티로 지정하고나니 일반적인 인스턴스 접근 방식으로는 해당 can't set attribute 라는 에러를 뿜뿜하며 접근할 수 없었다.

```python
>>> monster.name
# out : '파닥몬'
```
- 이렇게 얻은 '파닥몬'의 문자열 데이터는 클래스 멤버인 self.name에 직접 접근한 것이 아니라 프로퍼티로 같은 데이터 값의 사본을 출력해준 것이다.
- 솔직히 기존 코드가 손상됨으로써 오는 피해가 얼마나 막대한지 실감은 안 난다. 하지만 그렇다고 하니 비로소 납득하고 프로퍼티로 좋아요 개수를 세는 데이터에 접근해보겠다.

```python
# POST에 대한 좋아요 개수와 COMMENT에 대한 좋아요 개수 둘 다 필요하므로 두 모델에 추가했다.
def like_count(self):
    return self.like_users.count()
```
