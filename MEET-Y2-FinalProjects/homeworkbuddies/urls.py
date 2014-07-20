from django.conf.urls import patterns, url

from homeworkbuddies import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<assignment_id>\d+)/$', views.view_assignment, name='view_assignment'),
    url(r'^(?P<assignment_id>\d+)/post/$', views.post_message, name='post_message'),

)

