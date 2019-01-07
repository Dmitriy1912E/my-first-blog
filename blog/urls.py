from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<post_pk>\d+)/add/$', views.comment_new, name='comment_new'),
    url(r'^post/(?P<post_pk>\d+)/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[\w\-]+)/(?P<token>[\w]{1,13}-[\w]{1,20})/$',
        views.activate, name='activate'),
    url(r'^auth/login/$', views.login, name='user_login'),
    url(r'^auth/logout/$', views.logout, name='user_logout'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
