# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Post
from django.utils import timezone
from .form import PostForm
from django.shortcuts import render, get_object_or_404, redirect  # Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def post_list(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_write_form(request):
    form = PostForm()
    return render(request, 'blog/post_write_form.html', {'form': form})


def login_form(request):
    #로긴이 되어있는 경우에는 목록을 보여준다
    if request.user.is_authenticated():
        return redirect("/post_list")
    else:
        return render(request, 'blog/login_form.html')

    return render(request, 'blog/login_form.html')


def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
#    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

    return redirect('/login_form')


def post_edit_form(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_edit_form.html', {'post': post})


@csrf_exempt
def save_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_write_form.html', {'form': form})


@csrf_exempt
def login_action(request):

    username = request.POST.get("username", "denise77")
    password = request.POST.get("password", "1114")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('/post_list')
    else:
        # Return an 'invalid login' error message.
        return render(request, 'blog/login_form.html', {'message':'로긴에 실패했어요'})


def edit_post(request, pk):
    '''post edit action'''


    # fetch pk에 해당하는 post모델 인스턴를 가지고 온다.
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":

        # 폼모델  담는다 그리고 인스턴스 생성
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            ##post모델 인스턴스
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # 프로퍼티에 각자속성값을 담은 다음에 save
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit_form.html', {'form': form})


def delete_post(request, pk):
    '''delete_post action'''

    # pk에 해당하는 post객체 (Orm) blog_post테이블을 가지고 온다
    post = get_object_or_404(Post, pk=pk)  # 폼모델  담는다 그리고 인스턴스 생성
    post.id = pk
    post.delete()
    return redirect('/')


