from django.contrib.auth.models import  User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Identification_Number(models.Model):
    employee_id = models.IntegerField()

    def __str__(self):
        return str(self.employee_id)

class Content_Manager(models.Model):
    employee_id = models.IntegerField(default =0000)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name+" "+self.last_name+" "+str(self.employee_id)+" valid="+str(self.is_confirmed)

class Cluster(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

class Position(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname +' '+ self.lastname

class Tabulation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.candidate) + ' at '+ str(self.cluster) + ' has ' + str(self.votes) + ' votes.'


#======================NEWS CATEGORY====================================================

class News_category(models.Model):
    title= models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    tabindex = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class News (models.Model):
    category = models.ForeignKey(News_category,on_delete=models.CASCADE)
    headline = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    picture = models.ImageField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_bookmarked = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('index:news_detail', args=[slugify(self.category), slugify(self.headline), str(self.id)])

#======================LOG ENTRY=========================================================
class Modules (models.Model):
    module = models.CharField(max_length=50)
    module_desc = models.TextField()

    def __str__(self):
        return self.module

class Action_flag (models.Model):
    action = models.CharField(max_length=50)
    action_desc = models.TextField()

    def __str__(self):
        return self.action

class Activity_Log (models.Model):
    action_flag = models.ForeignKey(Action_flag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    affected_table = models.ForeignKey(Modules, on_delete=models.CASCADE)
    news_obj = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    tabs_obj = models.ForeignKey(Tabulation, on_delete=models.CASCADE,null=True)
    is_request = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user)+" "+str(self.action_flag)+" "+str(self.affected_table)+" "+str(self.datetime)

#=========================PROGRAMS===============================================

class Programs (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, default="")
    start = models.TimeField()
    end = models.TimeField()
    picture = models.ImageField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Keyword (models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword
#========================SHOP======================================================

class Products (models.Model):
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField()
    product_picture = models.ImageField()


#=======================LANDING PAGE===============================================
class Alignment(models.Model):
    align = models.CharField(max_length=10)

    def __str__(self):
        return self.align

class Landing_page (models.Model):
    image = models.ImageField()
    text = models.CharField(max_length=100, default="", blank=True)
    sub_text = models.CharField(max_length=150, default=" ", blank=True)
    text_alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE, default=1, blank=True)
    has_action = models.BooleanField(default=False)
    action_name = models.CharField(max_length=10, default="LEARN MORE", blank=True)
    action_url = models.CharField(max_length=500,default="#",blank=True)
    order = models.IntegerField(default=0)
    is_show = models.BooleanField(default=True)
    color = models

    def __str__(self):
        return "("+str(self.order)+") "+self.text +" id:"+ str(self.id)

#========================ADVERTISE==================================================
class is_agency_represented(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100, default=' ', blank=True)

    def __str__(self):
        return self.title

class Client (models.Model):
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    is_agency_represented = models.ForeignKey(is_agency_represented, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100, blank=True)
    your_position = models.CharField(max_length=100)
    contact_number = models.CharField(default='+63', max_length=15)
    email = models.EmailField()
    other_info = models.TextField(blank=True, default=' ')
    is_newsletter = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.brand_name+" "+str(self.datetime)


#============================================================================
class Page (models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default=' ')

    def __str__(self):
        return self.title

class Info (models.Model):
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    content = models.TextField()
    has_action = models.BooleanField(default=False)
    action_name = models.CharField(max_length=10, default="LEARN MORE", blank=True)
    action_url = models.CharField(max_length=500, default="#", blank=True)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('index:info', args=[slugify(self.page.title)])

#================================================================================

class ContactJACK_message (models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(default='+63', max_length=15)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name+" "+self.email+" "+str(self.datetime)

# class Visitor (models.Model):
#     account_id = models.IntegerField()
#     firstname = models.CharField(max_length=50)
#     middlename = models.CharField(max_length=50, blank=True)
#     lastname = models.CharField(max_length=50)
#     profile_picture = models.CharField(max_length=500)
#
#     def __str__(self):
#         return str(self.pk)+" - "+str(self.account_id)
#
# class Comment(models.Model):
#     user_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
#     activity_id = models.IntegerField()
#     content = models.TextField()
#     upvote = models.IntegerField()
#     downvote = models.IntegerField()
#     datetime = models.DateTimeField(auto_now_add=True, blank=True)
#
#     def __str__(self):
#         return str(self.pk)+" - "+str(self.user_id)+" -  "+str(self.datetime)
#
# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
#     content = models.TextField()
#     upvote = models.IntegerField()
#     downvote = models.IntegerField()
#     datetime = models.DateTimeField(auto_now_add=True, blank=True)
#
#     def __str__(self):
#         return str(self.pk)+" - "+str(self.user_id)+" - "+str(self.datetime)

class Live_File(models.Model):
    name = models.CharField(max_length=50, default="Live Files")
    audio_url = models.URLField()
    video_url = models.URLField(blank=True)
    is_live = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)