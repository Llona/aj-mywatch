from django.contrib import admin
from watch_list.models import Anime, WatchState, News

# Register your models here.
admin.site.register(Anime)
admin.site.register(WatchState)
admin.site.register(News)
