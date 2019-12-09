from django.http import HttpResponse
from django.urls import path
from . import views
from .sitemaps import NewsSitemap, StaticViewSitemap, InfoSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'news': NewsSitemap,
    'info':InfoSitemap,
    'static':StaticViewSitemap
}

app_name = 'index'

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: / \n\n Sitemap: http://jackradio.online/sitemap.xml", content_type="text/plain"), name="robots_file"),
    path('', views.index, name='index'),
    path('access_forbidden', views.forbidden, name='forbidden'),
    path('how-to-listen', views.how_to_listen, name='how_to_listen'),
    path('how-to-listen/radio', views.radio, name='radio'),
    # moderator
    path('moderator/register', views.register, name='register'),
    path('moderator/login_user', views.login_user, name='login_user'),
    path('moderator/logout_user', views.logout_user,name='logout_user'),
    path('moderator/user=<user_id>', views.mod, name='mod'),
    path('moderator/user=<user_id>/editor', views.compose_article, name='compose_article'),
    path('moderator/user=<user_id>/<news_id>/editor/?show=<show>', views.update_article, name='update_article'),
    path('moderator/user=<user_id>/news_list', views.news_list, name='news_list'),


    # news
    path('news', views.news, name='news'),
    path('news/<category>/<headline>)/id=<news_id>', views.news_detail, name='news_detail'),


    # tabulation
    path('bantay_piniliay2k19/cluster=<cluster_id>', views.candidates, name='candidates'),
    path('bantay_piniliay2k19/cluster=<cluster_id>/candidate=<candidate_id>', views.candidate_detail, name='detail'),

    # business
    path('advertise', views.advertise, name='advertise'),

    # videos
    path('video', views.video, name='videos'),
    path('video/<grouper>/<title>/id=<video_id>/status=<status>', views.video_detail, name='video_detail'),
    path('video/?list=<program>', views.video_list, name='video_list'),

    #info
    path('<page>', views.info, name='info'),


]
