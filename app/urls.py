from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'app.views.upload_home', name='main'),
    url(r'^upload$', 'app.views.upload', name='main'),
    url(r'^uploads$', 'app.views.recent_uploads', name='uploads'),
    url(r'^photo-search$', 'app.views.photo_search', name='search'),
    url(r'^search$', 'app.views.searchUploads', name='do_search'),
    url(r'^details$', 'app.views.folder_details', name='upload_detail'),
    url(r'^news$', 'app.views.news', name='news'),
    url(r'^news/(\d+)$', 'app.views.news_item', name='news_detail'),
    url(r'^media$', 'app.views.media', name='media'),
    url(r'^photos$', 'app.views.photos', name='photos'),
    url('^pages/', include('django.contrib.flatpages.urls')),
    url(r'^accounts/profile/', 'app.views.profile', name='profile'),

)