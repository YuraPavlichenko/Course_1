from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя користувача', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя користувача', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            'CATEGORY': forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']  # Це буде title з словнику cleaned_data
        if re.match(r'\d', title):
            raise ValidationError("Назва не може починатись з цифри")
        return title

    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        print(is_published)
        if is_published:
            return is_published
        else:
            raise ValidationError("Став галочку сука")

'''
# Форма, не зв'язана з моделлю
class NewsForm(forms.Form):
    # Віджити описують стиль форми
    title = forms.CharField(max_length=150, label='Назва', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5
    }))
    is_published = forms.BooleanField(label='Опубліковано?', initial=True)
    category = forms.ModelChoiceField(empty_label='Виберіть категорію', label='Категорія', queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))
'''