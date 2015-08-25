이달수 작업 내용 정리

1. 프로젝트 생성

1-1. workon pystagram

1-2. django-admin startproject myblog01

1-3. cd myblog01

1-4. python manage.py migrate

1-5. python manage.py createsuperuser

1-6. python manage.py runserver (서버 러닝 확인 및 어드민 페이지 로그인 확인)



2. blog 앱 생성

2-1. python manage.py startapp blog

2-2. myblog01/settings.py의 INSTALLED_APPS 에 'blog', 추가

2-3. blog/models.py (Post Model 정의)
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

2-4. blog/admin.py (어드민 페이지에 Post 등록)
from django.contrib import admin
from blog.models import Post

admin.site.register(Post)

2-5. myblog01/urls.py (blog urls 등록)
from django.conf.urls import include, url
from django.contrib import admin

from blog import urls as blog_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog_urls)), # "주소/blog" 로 접근하는 내용은 blog앱의 urls.py에 정의함
]

2-6. blog에 urls.py 생성 및 url 등록
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'blog.views.index'), # "주소/blog/" 로 접근하면 보여지는 index.html
    url(r'^(?P<pk>\d+)/$', 'blog.views.detail'), # "주소/blog/글번호" 로 접근하면 각 번호의 글이 보여지는 detail.html
    url(r'^new/$', 'blog.views.new'), # "주소/blog/new" 로 접근하면 새로운 글을 작성 할 수 있음
    url(r'^(?P<pk>\d+)/edit/$', 'blog.views.edit'), # "주소/글번호/edit" 로 접근하면 각 번호의 글을 수정할 수 있음
]

2-7. blog/views.py (index와 detail 구현)
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post


def index(request):
    post_list = Post.objects.all()

    lorempixel_categories = (
        "abstract", "animals", "business", "cats", "city", "food", "night",
        "life", "fashion", "people", "nature", "sports", "technics", "transport",
    )

    return render(request, 'blog/index.html', {
        'post_list': post_list,
        'lorempixel_categories': lorempixel_categories,
    })


def detail(request, pk):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post
    })

2-8. blog에 templates/blog에 index.html, detail.html, layout,html 생성

2-9. blog/templates/blog/layout.html 작성 (github에서 복사해서 편집함)
<!doctype html>
<html>
<head>
<meta charset="utf8" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" />
<link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.5/flatly/bootstrap.min.css" />
<style>
img {
    max-width: 100%;
}
.navbar {
    border-radius: 0;
}
#footer {
    background-color: #333333;
    line-height: 20px;
    padding: 30px 20px;
    margin-top: 60px;
}
</style>
{% block extra_head %}{% endblock %}
</head>
<body>

<div class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="{% url "blog.views.index" %}">Pystagram Blog</a>
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-top" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
        </div>
        <div id="navbar-top" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                {% block navbar_left %}
                {% endblock %}
            </ul>
            <ul class="nav navbar-nav navbar-right">
                {% block navbar_right %}
                    {% if not user.is_authenticated %}
                        <li><a href="/accounts/login/?next={{ request.path }}">로그인</a></li>
                        <li><a href="/accounts/signup/?next={{ request.path }}">회원가입</a></li>
                    {% else %}
                        <li><a href="/accounts/logout/?next={{ request.path }}">로그아웃</a></li>
                    {% endif %}
                {% endblock %}
            </ul>
        </div>
    </div>
</div>

{% block content %}
{% endblock %}

<div id="footer">
    <div class="container">
        <div class="row">
            <div class="col-sm-6 text-muted">
                파이썬 웹프레임워크인 <a href="http://djangoproject.com" target="_blank">Django</a> 로 만들었습니다.<br/>
            </div>
            <div class="col-sm-6 text-right">
                <a href="http://www.fastcampus.co.kr/" target="_blank">with fastcampus</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>

2-10. blog/templates/blog/index.html 작성 (github에서 복사해서 편집함)
{% extends "blog/layout.html" %}

{% block extra_head %}
<!-- 참고 : http://tobyyun.tumblr.com/post/55858430437/css%EB%A5%BC-%ED%86%B5%ED%95%9C-%EB%A9%80%ED%8B%B0%EB%9D%BC%EC%9D%B8-%EB%A7%90%EC%A4%84%EC%9E%84-%EC%B2%98%EB%A6%AC%EC%99%80-%ED%8F%B4%EB%B0%B1 -->
<style>
.thumbnail .caption h5 {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    word-wrap: break-wrap;
}
.thumbnail .caption {
    height: 50px;
}
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        {% for post in post_list %}
            <div class="col-xs-6 col-sm-4 col-md-3">
                <div class="thumbnail">
                    <a href="{% url "blog.views.detail" post.pk %}">
                        <img src="http://lorempixel.com/400/400/{{ lorempixel_categories|random }}/" class="img-rounded" />
                        <div class="caption">
                            <h5>{{ post.title }}</h5>
                        </div>
                    </a>
                </div>
            </div>
        {% endfor %}
    </div>
</div>
{% endblock %}

2-11. blog/templates/blog/detail.html 작성 (github에서 복사해서 편집함)
{% extends "blog/layout.html" %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-info">
                <div class="panel-heading">
                    {{ post.title }}
                </div>
                <div class="panel-body">
                    {{ post.content|linebreaks }}
                </div>
                <div class="panel-footer clearfix">
                    <div class="pull-right">
                        수정 : {{ post.updated_at }}<br>작성 : {{ post.created_at }}
                    </div>
                </div>
            </div>

            <a href="{% url "blog.views.index" %}" class="btn btn-default">글목록</a>
            <a href="{% url "blog.views.edit" post.pk %}" class="btn btn-info">수정</a>
        </div>
    </div>
</div>
{% endblock %}

2-12. python manage.py makemigrations blog

2-13. python manage.py migrate blog

2-14. python manage.py runserver (글이 없어서 내용은 안나오지만 layout은 잘 보이고 admin 페이지도 잘 나옴)

2-15. admin 페이지를 이용해서 Post 등록 (3개 등록 후 확인, 잘 나옴)

2-16. django-bootstrap3 설치 (pip를 이용해서 설치함) 후 myblog01/settings.py의 INSTALLED_APPS에 bootstrap3 추가

2-17. blog/templates/blog에 form.html 파일 만들기  (github에서 복사함)
{% extends "blog/layout.html" %}
{% load bootstrap3 %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-sm-12">
            <form action="" method="POST" class="form" enctype="multipart/form-data">
                {% csrf_token %}
                {% bootstrap_form form %}
                {% buttons %}
                    <button class="btn btn-primary">
                        {% bootstrap_icon "star" %} Submit
                    </button>
                {% endbuttons %}
            </form>
        </div>
    </div>
</div>
{% endblock %}

2-18. blog에 forms.py 파일 만들기
from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

2-19. blog/views.py (new와 edit 구현)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Post
from blog.forms import PostForm


def index(request):
    post_list = Post.objects.all()

    lorempixel_categories = (
        "abstract", "animals", "business", "cats", "city", "food", "night",
        "life", "fashion", "people", "nature", "sports", "technics", "transport",
    )

    return render(request, 'blog/index.html', {
        'post_list': post_list,
        'lorempixel_categories': lorempixel_categories,
    })


def detail(request, pk):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post
    })


@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {
        'form': form,
    })

2-20. blog/templates/blog/index.html 에 글쓰기 버튼 추가
{% extends "blog/layout.html" %}

{% block extra_head %}
<!-- 참고 : http://tobyyun.tumblr.com/post/55858430437/css%EB%A5%BC-%ED%86%B5%ED%95%9C-%EB%A9%80%ED%8B%B0%EB%9D%BC%EC%9D%B8-%EB%A7%90%EC%A4%84%EC%9E%84-%EC%B2%98%EB%A6%AC%EC%99%80-%ED%8F%B4%EB%B0%B1 -->
<style>
.thumbnail .caption h5 {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    word-wrap: break-wrap;
}
.thumbnail .caption {
    height: 50px;
}
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        {% for post in post_list %}
            <div class="col-xs-6 col-sm-4 col-md-3">
                <div class="thumbnail">
                    <a href="{% url "blog.views.detail" post.pk %}">
                        <img src="http://lorempixel.com/400/400/{{ lorempixel_categories|random }}/" class="img-rounded" />
                        <div class="caption">
                            <h5>{{ post.title }}</h5>
                        </div>
                    </a>
                </div>
            </div>
        {% endfor %}
    </div>
</div>
<div class="container">
    <div class="row">
        <div class="col-xs-6 col-sm-4 col-md-3">
            <a href="{% url "blog.views.new" %}" class="btn btn-success">글쓰기</a>
        </div>
    </div>
</div>
{% endblock %}

2-21. blog/models.py (Comment 모델 정의)
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

2-22. blog/admin.py (Comment 등록)
from django.contrib import admin
from blog.models import Post, Comment

admin.site.register(Post)

admin.site.register(Comment)

2-23. blog/forms.py (Comment폼 정의)
from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

2-24. blog/urls.py 수정 (댓글 관련 url 추가)
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'blog.views.index'), # "주소/blog/" 로 접근하면 보여지는 index.html
    url(r'^(?P<pk>\d+)/$', 'blog.views.detail'), # "주소/blog/글번호" 로 접근하면 각 번호의 글이 보여지는 detail.html
    url(r'^new/$', 'blog.views.new'), # "주소/blog/new" 로 접근하면 새로운 글을 작성 할 수 있음
    url(r'^(?P<pk>\d+)/edit/$', 'blog.views.edit'), # "주소/글번호/edit" 로 접근하면 각 번호의 글을 수정할 수 있음

    url(r'^(?P<pk>\d+)/comments/new/$', 'blog.views.comment_new'), # "주소/blog/글번호/comments/new" 로 접근하면 해당 글의 댓글을 추가 할 수 있음
    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/edit/$', 'blog.views.comment_edit'), # "주소/blog/글번호/comments/댓글번호/edit" 로 접근하면 해당 댓글을 수정할 수 있음
]

2-25. blog/views.py 에 comment_new와 comment_edit 추가
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.all()

    lorempixel_categories = (
        "abstract", "animals", "business", "cats", "city", "food", "night",
        "life", "fashion", "people", "nature", "sports", "technics", "transport",
    )

    return render(request, 'blog/index.html', {
        'post_list': post_list,
        'lorempixel_categories': lorempixel_categories,
    })


def detail(request, pk):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        raise Http404

    return render(request, 'blog/detail.html', {
        'post': post
    })


@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            return redirect('blog.views.detail', post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pk)
            comment.save()
            return redirect('blog.views.detail', pk)
    else:
        form = CommentForm()

    return render(request, 'blog/form.html', {
        'form': form,
    })

@login_required()
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog.views.detail', post_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/form.html', {
        'form': form,
    })

2-26. python manage.py makemigrations blog

2-27. python manage.py migrate blog

2-28. python manage.py runserver (일단 잘 동작합니다.)

2-29. blog/templates/blog/detail.html 에 댓글 관련 UI를 추가함
{% extends "blog/layout.html" %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-info">
                <div class="panel-heading">
                    {{ post.title }}
                </div>
                <div class="panel-body">
                    {{ post.content|linebreaks }}
                </div>
                <div class="panel-footer clearfix">
                    <div class="pull-right">
                        수정 : {{ post.updated_at }}<br>작성 : {{ post.created_at }}
                    </div>
                </div>
            </div>

            <ul>
                {% for comment in post.comment_set.all %}
                    <li>
                        {{ comment.content }}
                        <a href="{% url "blog.views.comment_edit" post.pk comment.pk %}">Edit</a>
                    </li>
                {% endfor %}
            </ul>

            <a href="{% url "blog.views.index" %}" class="btn btn-default">글목록</a>
            <a href="{% url "blog.views.edit" post.pk %}" class="btn btn-info">수정</a>
            <a href="{% url "blog.views.comment_new" post.pk %}" class="btn btn-success">새 댓글</a>
        </div>
    </div>
</div>
{% endblock %}

2-30. myblog01/settings.py의 TEMPLATES의 DIRS에 'myblog01/templates' 추가 및 blog/layout.html과 blog/form.html 파일을 myblog01/templates로 복사 한 후 blogy/layout.html과 blog/form.html은 myblog01/templates에 있는 파일들을 상속받음
'DIRS': ['myblog01/templates'],
{% extends "layout.html" %}


3. account 앱 생성

3-1. python manage.py startapp accounts

3-2. accounts/models.py 에 UserProfile 추가 (User와 1:1 관계를 맺음)
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    biography = models.TextField(default='')

3-3. myblog01/settings.py의 INSTALLED_APPS에 'accounts' 추가

3-4. myblog01/urls.py에 accounts로 접근하는 url에 대한 정의 추가
from django.conf.urls import include, url
from django.contrib import admin

from blog import urls as blog_urls
from accounts import urls as accounts_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog_urls)), # "주소/blog" 로 접근하는 내용은 blog앱의 urls.py에 정의함
    url(r'^accounts/', include(accounts_urls)), # "주소/accounts" 로 접근하는 내용은 accounts앱의 urls.py에 정의함
]

3-5. accounts에 urls.py 추가

----- 여기까지 작업했습니다. -----