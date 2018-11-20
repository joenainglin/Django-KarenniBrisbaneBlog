from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed



app_name = 'Post'
urlpatterns = [
		# map to Post list view
		url(r'^$', views.Post_list, name = 'Post_list'),
		#url(r'^$', views.PostListView.as_view(), name = 'Post_list'),
		url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.Post_list_by_tag, name='Post_list_by_tag'),
		# category 
		url(r'^category/(?P<category_name>[-\w]+)/$',views.Post_list_by_category, name='Post_list_by_category'),
		# map to post detail view
		url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
			views.Post_detail, name = 'Post_detail'),
		url(r'^(?P<post_id>\d+)/share/$', views.Post_share, name='Post_share'),
		url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
		url(r'^search/', views.post_search, name='post_search'),
		url(r'^new/', views.post_new, name='post_new'),
		url(r'^edit/(?P<slug>[-\w]+)/$', views.post_edit, name='post_edit'),
		url(r'^delete/(?P<slug>[-\w]+)/$',views.post_delete, name='post_delete'),

] 