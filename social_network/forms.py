from django import forms
from django.contrib.auth import password_validation
from .apps import user_registered
from django.core.exceptions import ValidationError

from .models import PostUser, Post


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Email address')
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput,
                                help_text='enter password again')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        print(password1)
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        print(password1)
        print(password2)

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('password not match',
                                                   code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        print('set pass')
        print(self.cleaned_data['password1'])
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        # user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = PostUser
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}
