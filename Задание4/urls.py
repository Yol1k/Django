"""
Definition of urls for Задание4.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('resources/', views.resources, name='resources'),
    path('forums/', views.forums, name='forums'),
    path('pool/', views.pool, name='pool'),
    path('registration/', views.registration, name= 'registration'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('category/', views.category, name='category'),
    path('category/<int:parametr>/', views.category_elements, name='category_elements'),
    path('category/element/<int:parametr>/', views.element, name='element'),
    path('category/add_category/', views.newcategory, name='newcategory'),
    path('category/add_element/', views.newelement, name='newelement'),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()