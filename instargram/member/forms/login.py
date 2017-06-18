from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
              'placeholder': '아이디를 입력해주세요.',
            },
        ),
    )

    password = forms.CharField(
      widget=forms.PasswordInput(
          attrs={
              'placeholder': '비밀번호를 입력해주세요.'
          }
      )
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login credentials not valid!'
            )

        return self.cleaned_data

