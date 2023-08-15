from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db.models import F
from django.template import loader
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class HomeView(generic.ListView):
    template_name = "twitter/home.html"
    context_object_name = "post_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
def HomeView(request):
    if(request.user.is_authenticated == False):
        return redirect('login')
    else:
        post_list = Post.objects.order_by("-pub_date")[:50]
        context = {"post_list": post_list}
        return render(request, "twitter/home.html", context)

def ProfileView(request, username):
    tempUser = get_object_or_404(User2, username=username)
    currUser = get_object_or_404(User2, username=request.user.username)
    followed = False
    tempFollow = get_object_or_404(FollowObj, username=username)
    if currUser.following.filter(username=username).exists():
        followed = True 
    # post_list = loader(tempUser.post.objects.order_by("pub-date")[:5])
    post_list = Post.objects.filter(user = tempUser).order_by("-pub_date")
    context = {"post_list": post_list, "username": username, "followed": followed, "user": tempUser}
    return render(request, "twitter/profile.html", context)

def PostView(request, pk):
    tempPost = get_object_or_404(Post, pk=pk)
    user = get_object_or_404(User2, username=request.user.username)
    liked = False
    own = False
    if tempPost.likedBy.filter(username=user.username).exists():
        liked = True
    if tempPost.user.username == user.username:
        own = True
    if request.method == "POST":
        if request.POST['comment'] != "": 
            user2 = User2.objects.filter(username = request.user.username)
            text = request.POST['comment']
            tempComment = Comment.objects.create(text = text, user = user2[0], pub_date = timezone.now(), post = Post.objects.get(pk=pk))
            tempComment.save() 
            tempPost.commentsCount += 1
            tempPost.save()
            return redirect('post', pk = pk)
    context = {"post": tempPost, "liked": liked, "own": own}
    return render(request, 'twitter/post.html', context)

def CommentView(request, pk):
    tempComment = get_object_or_404(Comment, pk=pk)
    user = get_object_or_404(User2, username = request.user.username)
    liked = False; own = False; postLiked = False
    if tempComment.likedBy.filter(username=user.username).exists():
        liked=True
    if tempComment.user.username == user.username:
        own = True
    if tempComment.post.likedBy.filter(username=user.username).exists():
        postLiked = True
    if request.method == "POST":
        if request.POST['comment'] != "":
            user2 = User2.objects.filter(username = request.user.username)
            text = request.POST['comment']
            tempCommentPlus = CommentUnderComment.objects.create(text = text, user=user2[0], pub_date=timezone.now(), post = Comment.objects.get(pk=pk))
            tempCommentPlus.save()
            tempComment.comments += 1
            tempComment.save() 
            return redirect('comment', pk=pk)
    context = {"comment": tempComment, "liked": liked, "own": own, "postliked": postLiked}
    return render(request, 'twitter/comment.html', context)

def PostLike(request, pk):
    user = get_object_or_404(User2, username=request.user.username)
    post = get_object_or_404(Post, pk=pk)
    if post.likedBy.filter(username=user.username).exists():
        post.likedBy.remove(user)
        post.likes = post.likes-1 
    else: 
        post.likedBy.add(user)
        post.likes = post.likes+1 
    post.save()
    return HttpResponseRedirect(reverse('post', args=[int(pk)]))

def CommentLike(request, pk):
    user = get_object_or_404(User2, username=request.user.username)
    comment = get_object_or_404(Comment, pk=pk)
    if comment.likedBy.filter(username=user.username).exists():
        comment.likedBy.remove(user)
        comment.likes = comment.likes-1
    else: 
        comment.likedBy.add(user)
        comment.likes = comment.likes+1 
    comment.save() 
    return HttpResponseRedirect(reverse('comment', args=[int(pk)]))

def DeletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete() 
    return HttpResponseRedirect(reverse('home'))

def DeleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete() 
    return HttpResponseRedirect(reverse('home'))

def CreatePost(request):
    user = get_object_or_404(User2, username=request.user.username)
    text = request.POST['text']
    newpost = Post.objects.create(user=user, text=text, pub_date=timezone.now())
    newpost.save()
    user.posts += 1
    user.save() 
    return HttpResponseRedirect(reverse('home'))

def Following(request):
    user = get_object_or_404(User2, username=request.user.username)
    userlist = []
    for x in user.following.all():
        userlist.append(User2.objects.get(username=x.username))
    postlist = Post.objects.filter(user__in = userlist).order_by("-pub_date")
    context = {"accountlist": userlist, "postlist": postlist}
    return render(request, 'twitter/following.html', context)

def Follow(request, username):
    user = get_object_or_404(User2, username=request.user.username)
    user2 = get_object_or_404(User2, username=username)
    if user.following.filter(username=user2.username).exists():
        user.following.remove(FollowObj.objects.get(username=username))
        user.followers -= 1
        user2.followingNum -=1 
    else:
        user.following.add(FollowObj.objects.get(username=username))
        user.followers += 1
        user2.followingNum +=1 
    user.save()
    user2.save() 
    return HttpResponseRedirect(reverse('profile', args=[str(username)]))

def LogIn(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong Login Details")
            return redirect('login')
    return render(request, 'twitter/login.html')

def SignUp(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            found = False
            users = User2.objects.all()
            for x in users:
                if x.username == username:
                    found = True
            if found == False: 
                myuser = User.objects.create_user(username=username, password=password)
                myuser.save()
                myuser2 = User2.objects.create(username=username, password=password)
                myuser2.save()
                myfollow = Follow.objects.create(username=username)
                myfollow.save()
                return redirect(LogIn)
            else:
                messages.error(request, "Username already in use")
                return redirect('signup')
        else:
            messages.error(request, "Passwords Don't Match") 
            return redirect('signup')
    return render(request, 'twitter/signup.html')

def SignOut(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('login')
# def home(request):
#     return HttpResponse("Hello World, You're at the main screen")
