from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.
"""
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)
"""


class Anime(models.Model):
    watch_state = models.ManyToManyField(User, through='WatchState')
    creator = models.ForeignKey(User, related_name='+', null=True)
    name = models.CharField(max_length=100)
    origin_name = models.CharField(max_length=100, blank=True)
    total = models.IntegerField(null=True, blank=True)
    media_type = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=20, blank=True)
    publication_date = models.CharField(max_length=20, blank=True)
    url = models.CharField(max_length=300, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    summary = models.TextField(max_length=2000, blank=True)
    modify_date = models.DateTimeField(default=(datetime.utcnow() + timedelta(hours=8)), null=True)
    add_date = models.DateTimeField(default=(datetime.utcnow() + timedelta(hours=8)), null=True)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class WatchState(models.Model):
    user = models.ForeignKey(User)
    anime = models.ForeignKey(Anime)
    watch_last_date = models.DateTimeField(default=(datetime.utcnow() + timedelta(hours=8)), null=True)
    num_of_chapter = models.CharField(max_length=50, blank=True, )
    watch_state = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.num_of_chapter)

    def __str__(self):
        return str(u'%s %s %s %s' % (self.user, self.anime, self.num_of_chapter, self.watch_state))


class News(models.Model):
    date = models.DateTimeField(default=datetime.utcnow() + timedelta(hours=8))
    # date_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    # .strftime('%Y-%m-%d %H:%M:%S')
    news_type = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return str(self.date)

    def __str__(self):
        return str(u'%s %s' % (self.date, self.news_type))

# for test, need remove=====
class photo(models.Model):
    owner = models.ForeignKey(User)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.owner, self.image)

    def __str__(self):
        return '%s %s' % (self.owner, self.image)
# =====
