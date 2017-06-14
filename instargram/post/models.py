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

    like_users = models.ManyToManyField(
        User,
        through='PostLike',
        related_name='like_posts',
    )

    def add_comment(self, user, content):
        return self.post_set.create(author=user, content=content)

    def like_count(self):
        return self.like_users.count()


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

    like_users = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='like_comments',
    )

    def like_count(self):
        return self.like_users.count()


class CommentLike(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    pass
