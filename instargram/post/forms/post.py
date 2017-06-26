from django import forms

from post.models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

        if self.instance.my_comment:
            self.fields['comment'].initial = self.instance.my_comment

    # Post 객체가 아닌 Comment 객체 생성 요소, post.my_comment 와 OTO 관계
    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment'
        )

    def save(self, **kwargs):

        commit = kwargs.get('commit', True)
        author = kwargs.pop('author', None)

        if not self.instance.pk:
            self.instance.author = author

        instance = super().save(**kwargs)
        print("1.", instance.author)
        print("2.", instance.pk)
        print("3.", instance.my_comment)
        comment_string = self.cleaned_data['comment']

        if commit and comment_string:
            if instance.my_comment:
                instance.my_comment.content = comment_string
                instance.my_comment.save()
            else:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=author,
                    content=comment_string,
                )
            # instance.save()
        return instance
