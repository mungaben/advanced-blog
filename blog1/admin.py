from atexit import register
from sqlite3 import register_adapter
from tokenize import Comment
from django.contrib import admin
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title',"slug",'author',"publish","status"]
    list_filter=['status','created','publish','author']
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=('status','publish',)

@admin.register(Comment)
class Admin(admin.ModelAdmin):
    list_display=["name","email","created","updated","active"]
    list_filter=["active","updated","created"]
    search_fields=["created","active","name","email","body"]
    

    
    


# Register your models here.
