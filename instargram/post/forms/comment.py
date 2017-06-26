from django import forms
from django.core.exceptions import ValidationError

from post.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]

        content = forms.TextInput(

        )

    def clean_comment(self):
        comment_string = self.cleaned_data['content']
        if len(comment_string) < 3:
            raise ValidationError(
                '댓글은 최소 3자 이상 입력해야합니다.'
            )

        return comment_string
