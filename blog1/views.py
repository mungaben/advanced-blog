from ast import Try
from contextvars import Context
from email import message
from multiprocessing import context
from wsgiref.util import request_uri
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

def post_list(request,tag_slug=None):
    post=Post.objects.all()
    object_list=post
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tag__in=[tag])
    paginator=Paginator(object_list,3)#3 published post/object_list 
    #for each page
    page=request.GET.get('page')#current page
    try:
        post=paginator.page(page)#get objects of desired page use page() method
        
    except PageNotAnInteger:
        #IF NOT DELIVER THE FIRST PAGE
        post=paginator.page(1)
        
    except EmptyPage:
        #if page out of range give lat page
        post=paginator.page(paginator.num_pages)
    context={
        "page":page,
        "post":post,
        'tag':tag,
    }
    return render(request, "post/list.html", context)
    

def Post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,staus='published',
                           publish__year=year,publish__month=month,
                           publish__day=day)
    #get all post.tags ids ,value_list returns a tuple and we need it flat like 1,2,3so flat=true
    post_tag_id=post.tags.value_list("id",flat=True)
    #get posts with the tag ids .exclude post.id current post id
    similar_posts=post.all.filter(tag__in=post_tag_id).exclude(id=post.id)
    
    similar_posts=similar_posts.annotate(same_tag=Count("tags")).order_by('-same_tag','publish')[:4]
    
    
    comment=Comment.object.all(active=True)
    new_comment=None
    form=CommentForm()
    if request.method=="POST":
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=CommentForm.save(commit=False)
            new_comment.post=post
            new_comment.save()
        
    context={
        "post":post,
        "form":form,
        "comment":comment,
        "new_comment":new_comment,
        "similar_posts":similar_posts,
    }
    return render(request, "post/detail.html", context)
    
    
def Post_share(request,post_id):
    #get published post by post_id 
    post=get_object_or_404(Post,id=post_id,status='published')
    
    if request.method=='POST':
        sent=False
        form=EmailPostForm(request.POST)
        
        if form.is_valid():
            cd=form.cleaned_data
            #sendmail
            #we need a link to post in email..get abolute path of post using
            # get_absolute_url 
            # use request.build_absolute_uri() to build complete url including http schema s
            post_url=request.build_absolute_uri(post.get_absolute_url)
            subject=f"read the following {cd['name']} {post.title}"
            to='mungaben47@gmail.com'
            message=f"{post.title},{post.url},cd[name],{cd['comment']}"
            send_mail(subject,message,"mungaben21@gmail.com",to)
            sent=True
    else:
        form=EmailPostForm()
        
    context={
        "post":post,
        "form":form
    }
    
    return render(request, "post/share.html", context)
    
        
# Create your views here.
