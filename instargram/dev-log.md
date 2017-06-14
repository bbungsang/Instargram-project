### 0. 어플리케이션 'post'를 생성하고, settings.py에 등록

### 1. 모델 설계하기

### 2. 그린 모델과 필드를 작성하고 마이그레이션을 시도
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
- 아래와 같은 에러 발생

```python
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
