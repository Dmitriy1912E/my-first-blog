from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [

    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<post_pk>\d+)/add/$', views.comment_new, name='comment_new'),
    url(r'^post/(?P<post_pk>\d+)/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='/'), name='/'),
    url(r'^auth/login/$', views.login, name='user_login'),
    url(r'^auth/logout/$', views.logout, name='user_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
