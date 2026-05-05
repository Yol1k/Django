from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Comment, Blog, Category, Element

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class SiteReviewForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        min_length=2,
        max_length=50
    )

    age = forms.IntegerField(
        label='Ваш возраст',
        min_value=10,
        max_value=100,
        required=False
    )

    email = forms.EmailField(
        label='Электронная почта',
        required=False
    )

    site_rating = forms.ChoiceField(
        label='Общая оценка сайта',
        choices=[
            ('5', 'Отлично'),
            ('4', 'Хорошо'),
            ('3', 'Удовлетворительно'),
            ('2', 'Плохо'),
        ],
        widget=forms.RadioSelect
    )

    favorite_section = forms.ChoiceField(
        label='Какой раздел сайта вам нравится больше всего?',
        choices=[
            ('news', 'Новости'),
            ('blogs', 'Блоги'),
            ('forum', 'Форум'),
            ('resources', 'Полезные ресурсы'),
        ]
    )

    liked_features = forms.MultipleChoiceField(
        label='Что вам нравится на сайте?',
        required=False,
        choices=[
            ('Дизайн', 'Дизайн'),
            ('Содержание', 'Содержание'),
            ('Скорость работы', 'Скорость работы'),
            ('Навигация', 'Навигация'),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    subscribe = forms.BooleanField(
        label='Хочу получать обновления сайта',
        required=False
    )

    wishes = forms.CharField(
        label='Ваши пожелания',
        required=False,
        min_length=5,
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})
    )

class CommentForm (forms.ModelForm):

    class Meta:

        model = Comment

        fields = ('text',)

        labels = {'text': "Комментарий"}

class BlogForm (forms.ModelForm):

    class Meta:

        model = Blog

        fields = ('title', 'description', 'content', 'image')

        labels = {'title': "Новый блог", 'description':'Краткое содержание', 'content':'Полное содержание', 'image':'Картинка'}

class CategoryForm (forms.ModelForm):

    class Meta:

        model = Category

        fields = ('title', 'description')

        labels = {'title': "Новая категория", 'description':'Описание категории'}

class ElementForm (forms.ModelForm):

    class Meta:

        model = Element

        fields = ('title', 'description', 'content', 'price', 'image', 'category')

        labels = {'title': "Новый элемент категории", 'description':'Краткое описание элемента', 'content':'Полное описание элемента', 'price':'Цена элемента', 'image':'Картинка', 'category':'Категория элемента'}
