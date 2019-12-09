import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News, Info

class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    lastmod = datetime.datetime.now()
    def items(self):
        return News.objects.all()

class InfoSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5
    lastmod = datetime.datetime.now()

    def items(self):
        return Info.objects.all()
class StaticViewSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5
    lastmod = datetime.datetime.now()
    def items(self):
        return ['index:advertise', 'index:how_to_listen', 'index:radio', 'index:register', 'index:login_user', 'index:news','index:videos']
    def location(self, item):
        return reverse(item)