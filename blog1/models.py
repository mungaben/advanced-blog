
from curses import meta
from email.policy import default
from lib2to3.pgen2.token import COMMENT
from xml.etree.ElementTree import Comment
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    STATUS_CHOICES = (
       ('draft', 'Draft'),
       ('published', 'Published'),
       )
    title = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 50,unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField( auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 150,choices=STATUS_CHOICES,default='draft')
    tags=TaggableManager()
    
    
    class Meta:
        ordering=('-publish',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,
                                                self.publish.day,self.slug])
    
    def __str__(self): 
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments" ,on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    body= models.TextField()
    email = models.EmailField(max_length=250)
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField( auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering=("-created",)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    
    
    

    def __str__(self):
        return self.comment

   


    
    
    
    
    
    
    
    
    



# Create your models here.
