from datetime import datetime
from functools import cache
from django.shortcuts import render, redirect
from django.http import HttpRequest
from datetime import datetime
from .forms import SiteReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import models
from .models import Blog, Category, Element
from .models import Comment
from .forms import CommentForm, BlogForm, ElementForm, CategoryForm

def home(request):
    """Рендерит домашнюю страницу."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя Страница',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О Нас',
            'message':'Страница с описанием вашего приложения.',
            'year':datetime.now().year,
        }
    )

def resources(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )

def forums(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/forums.html',
        {
            'title': 'Форумы',
            'year': datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = SiteReviewForm(request.POST)

        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['age'] = form.cleaned_data['age']
            data['email'] = form.cleaned_data['email']
            data['site_rating'] = form.cleaned_data['site_rating']
            data['favorite_section'] = form.cleaned_data['favorite_section']
            data['liked_features'] = form.cleaned_data['liked_features']
            data['subscribe'] = form.cleaned_data['subscribe']
            data['wishes'] = form.cleaned_data['wishes']

            return render(
                request,
                'app/pool.html',
                {
                    'title': 'Обратная связь',
                    'year': datetime.now().year,
                    'form': None,
                    'data': data,
                }
            )
    else:
        form = SiteReviewForm()

    return render(
        request,
        'app/pool.html',
        {
            'title': 'Обратная связь',
            'year': datetime.now().year,
            'form': form,
        }
    )

def registration(request):
    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы

        regform = UserCreationForm (request.POST)

        if regform.is_valid(): #валидация полей формы

            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы

            reg_f.is_staff = False # запрещен вход в административный раздел

            reg_f.is_active = True # активный пользователь

            reg_f.is_superuser = False # не является суперпользователем

            reg_f.date_joined = datetime.now() # дата регистрации

            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных

            login(request, reg_f)

            return redirect('home') # переадресация на главную страницу после регистрации

    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    return render(
        request,
        'app/registration.html',
        {
        'regform': regform, # передача формы в шаблон веб-страницы
        'year':datetime.now().year,
        }
)

def blogs(request):

    assert isinstance(request, HttpRequest)

    posts = Blog.objects.all()

    return render(
        request,
        'app/blogs.html',
        {
            'title':'Блог',
            'posts': posts,
            'year': datetime.now().year, 
        }
    )

def blogpost(request, parametr):

    assert isinstance(request, HttpRequest)

    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment_f = form.save(commit=False)

            comment_f.author = request.user

            comment_f.date = datetime.now()

            comment_f.post = Blog.objects.get(id=parametr)

            comment_f.save()

            return redirect('blogpost', parametr=post.id)

    else:

        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
        'post': post,
        'year': datetime.now().year,
        'comments': comments,
        'form': form, 
        }
    )

def newpost(request):

    assert isinstance(request, HttpRequest) 

    if request.method == "POST":

        blogform = BlogForm(request.POST, request.FILES)

        if blogform.is_valid():

            blog_f = blogform.save(commit=False)

            blog_f.author = request.user

            blog_f.posted = datetime.now()

            blog_f.save()

            return redirect('blogs')

    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Создать новый блог',
            'year': datetime.now().year, 
        }
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Страница с видео.',
            'year':datetime.now().year,
        }
    )

def category(request):

    assert isinstance(request, HttpRequest)

    categories = Category.objects.all()

    return render(
        request,
        'app/category.html',
        {
            'title':'Категории',
            'categories': categories,
            'year': datetime.now().year, 
        }
    )

def category_elements(request, parametr):

    category = Category.objects.get(id=parametr)
    elements = Element.objects.filter(category=category)
    return render(
        request,
        'app/category_elements.html',
        {
            'title': f'Товары в категории: {category.title}',
            'category': category,
            'elements': elements,
            'year': datetime.now().year,
        }
    )

def element(request, parametr):
    element = Element.objects.get(id=parametr)
    return render(
        request,
        'app/element.html', 
        {
            'title': element.title,
            'element': element,
            'year': datetime.now().year,
        }
    )

def newcategory(request):

    assert isinstance(request, HttpRequest) 

    if request.method == "POST":

        categoryform = CategoryForm(request.POST)

        if categoryform.is_valid():

            category_f = categoryform.save(commit=False)

            category_f.save()

            return redirect('category')

    else:
        categoryform = CategoryForm()

    return render(
        request,
        'app/newcategory.html',
        {
            'categoryform': categoryform,
            'title': 'Создать новую категорию',
            'year': datetime.now().year, 
        }
    )

def newelement(request):

    assert isinstance(request, HttpRequest) 

    if request.method == "POST":

        elementform = ElementForm(request.POST, request.FILES)

        if elementform.is_valid():

            element_f = elementform.save(commit=False)

            element_f.save()

            return redirect('category')

    else:
        elementform = ElementForm()

    return render(
        request,
        'app/newelement.html',
        {
            'elementform': elementform,
            'title': 'Создать новый элемент категории',
            'year': datetime.now().year, 
        }
    )