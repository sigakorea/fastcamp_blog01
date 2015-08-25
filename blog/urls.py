from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'blog.views.index'), # "주소/blog/" 로 접근하면 보여지는 index.html
    url(r'^(?P<pk>\d+)/$', 'blog.views.detail'), # "주소/blog/글번호" 로 접근하면 각 번호의 글이 보여지는 detail.html
    url(r'^new/$', 'blog.views.new'), # "주소/blog/new" 로 접근하면 새로운 글을 작성 할 수 있음
    url(r'^(?P<pk>\d+)/edit/$', 'blog.views.edit'), # "주소/글번호/edit" 로 접근하면 각 번호의 글을 수정할 수 있음

    url(r'^(?P<pk>\d+)/comments/new/$', 'blog.views.comment_new'), # "주소/blog/글번호/comments/new" 로 접근하면 해당 글의 댓글을 추가 할 수 있음
    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/edit/$', 'blog.views.comment_edit'), # "주소/blog/글번호/comments/댓글번호/edit" 로 접근하면 해당 댓글을 수정할 수 있음
]
