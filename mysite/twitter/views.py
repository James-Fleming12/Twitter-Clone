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
    # post_list = loader(tempUser.post.objects.order_by("pub-date")[:5])
    post_list = Post.objects.filter(user = tempUser).order_by("-pub_date")
    context = {"post_list": post_list}
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
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

def DeletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete() 
    return HttpResponseRedirect(reverse('home'))

def CreatePost(request):
    user = get_object_or_404(User2, username=request.user.username)
    text = request.POST['text']
    newpost = Post.objects.create(user=user, text=text, pub_date=timezone.now())
    newpost.save()
    return HttpResponseRedirect(reverse('home'))
    
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
            users = User2.objects
            for x in users:
                if x.username == username:
                    found = True
            if found == False: 
                myuser = User.objects.create_user(username=username, password=password)
                myuser.save()
                myuser2 = User2.objects.create(username=username, password=password)
                myuser2.save()
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
