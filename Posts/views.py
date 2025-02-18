from django.shortcuts import render, redirect, get_object_or_404
from Posts.forms import PostForm, CommentForm
from Posts.models import Post, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def home(request):

    posts = Post.objects.all().select_related('author')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'Blog/home.html', {'page_obj': page_obj})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'Blog/user_profile.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
        
    else:
        form = PostForm()
    return render(request, 'Blog/post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.view_count += 1
    post.save()

    is_liked = post.liked_users.filter(id=request.user.id).exists()

    comments = post.comment_set.all().order_by('-created_at').select_related('author')

    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post.pk)
        
        else:
            messages.error(request, 'Invalid comment.')

    else:
        comment_form = CommentForm()

    return render(
        request, 
        'Blog/post_detail.html', 
        {
            'post': post,
            'comments': comments,
            'form': comment_form,
            'is_liked': is_liked,
        }

    )


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'Blog/post_form.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('my_posts')


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment,  pk=comment_id, author=request.user)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('post_detail', pk=comment.post.id)


def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment,  pk=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', pk=comment.post.id)
        else:
            messages.error(request, 'Invalid comment.')
    
    return redirect('post_detail', pk=comment.post.id)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.liked_users.filter(id=request.user.id).exists():
        post.liked_users.remove(request.user)

    else:
        post.liked_users.add(request.user)

    return redirect('post_detail', pk=post_id)




        
    





