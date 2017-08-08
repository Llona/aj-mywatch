from django.conf.urls import include, url
from django.contrib import admin
from watch_list.views import watch_list_page, watch_data, watch_all_data, watch_add, \
    watch_search, search_add, auto_update_item_only, index

from django.views.static import serve
from .settings import MEDIA_ROOT

# for test, need remove
from watch_list.views import anime_watch_page, test, index, comment, upload_image

#from watch_list.views import index
#from django.contrib.auth.views import logout
#from django.views.generic import TemplateView

urlpatterns = [
    url(r'^my_watch/$', watch_list_page),
    url(r'^watch_data/(\d+)/$', watch_data),
    url(r'^watch_data/$', watch_all_data),
    url(r'^search_add/$', search_add),
    url(r'^watch_add/$', watch_add),
    url(r'^$', index),
    url(r'^item_search/$', watch_search),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^auto_update_item/', auto_update_item_only),

    # url(r'^watch_add_cover/$', watch_add_cover),

    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^accounts/logout/$', 'accounts.views.logout', name='logout'),

    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    # url(r'^accounts/register/$', 'accounts.views.register', name='register'),
    # url(r'^accounts/profile/$', TemplateView.as_view('template':'registration/profile.html'}, name='user_profile'),
    url(r'^admin/', include(admin.site.urls)),
    # MEDIA_ROOT path
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # ===for test, need remove===
    url(r'^upload/', upload_image, name='upload_image'),
    url(r'^animation/$', anime_watch_page),
    # url(r'^$', index, name='home'),
    url(r'^comment/$', comment, name='comment'),
    url(r'^test/$', test),
    # ===
]
