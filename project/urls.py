from django.conf.urls import include, url
from django.contrib import admin
from watch_list.views import watch_list_page, watch_data, watch_all_data, watch_add, \
    watch_search, search_add, auto_update_item_only, index_home

from django.views.static import serve
from .settings import MEDIA_ROOT

from welcome.views import index, health

urlpatterns = [
    url(r'^my_watch/$', watch_list_page),
    url(r'^watch_data/(\d+)/$', watch_data),
    url(r'^watch_data/$', watch_all_data),
    url(r'^search_add/$', search_add),
    url(r'^watch_add/$', watch_add),
#    url(r'^$', index_home),
    url(r'^item_search/$', watch_search),

    url(r'^accounts/', include('allauth.urls')),
	
	

    url(r'^auto_update_item/', auto_update_item_only),
    url(r'^$', index),
    url(r'^health$', health),


    url(r'^admin/', include(admin.site.urls)),
    # MEDIA_ROOT path
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
