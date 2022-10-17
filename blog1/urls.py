from django.urls import path
from .views import post_list,Post_detail,Post_share
app_name="blog1"
urlpatterns = [
    path("",post_list,name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         Post_detail,name='post_detail'),
    path('<int:post_id>/share',Post_share,name='post_share'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
]
