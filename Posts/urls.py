from django.urls import path
from Posts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('create_post', views.create_post, name='create_post'),
    path('post_detail/<int:pk>', views.post_detail, name='post_detail'),
    path('update_post/<int:pk>', views.update_post, name='update_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('like_post/<int:post_id>', views.like_post, name='like_post'),

]
