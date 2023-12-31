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
    own = False
    if tempUser == currUser:
        own = True
    if currUser.following.filter(username=username).exists():
        followed = True 
    # post_list = loader(tempUser.post.objects.order_by("pub-date")[:5])
    post_list = Post.objects.filter(user = tempUser).order_by("-pub_date")
    context = {"post_list": post_list, "username": username, "followed": followed, "user": tempUser, "own": own}
    return render(request, "twitter/profile.html", context)

def PostView(request, pk):
    tempPost = get_object_or_404(Post, pk=pk)
    user = get_object_or_404(User2, username=request.user.username)
    liked = False; own = False; bookmarked = False 
    userlists = user.ownlists.all(); nolists = False
    if tempPost.likedBy.filter(username=user.username).exists():
        liked = True
    if tempPost.user.username == user.username:
        own = True
    if user.bookmarks.filter(pk=tempPost.pk).exists(): 
        bookmarked = True
    if len(userlists) == 0:
        nolists = True
    if request.method == "POST":
        if request.POST['comment'] != "": 
            user2 = User2.objects.filter(username = request.user.username)
            text = request.POST['comment']
            tempComment = Comment.objects.create(text = text, user = user2[0], pub_date = timezone.now(), post = Post.objects.get(pk=pk))
            tempComment.save() 
            tempPost.commentsCount += 1
            tempPost.save()
            return redirect('post', pk = pk)
    context = {"post": tempPost, "liked": liked, "own": own, "bookmarked": bookmarked, "userlists": userlists, "nolists": nolists}
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
    noti = Notification.objects.create(postUser = user, recieveUser = post.user, text = user.username + " has liked one of your posts") 
    noti.save() 
    post.user.notificationlist.add(noti)
    post.user.save() 
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
    noti = Notification.objects.create(postUser = user, recieveUser = comment.user, text=user.username + " has liked one of your comments")
    noti.save() 
    comment.user.notificationlist.add(noti)
    comment.user.save() 
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

def CreateList(request): 
    user = get_object_or_404(User2, username=request.user.username)
    name = request.POST['name']
    desc = request.POST['desc']
    if name != None and desc != None: 
        newlist = PostList.objects.create(user=user, name=name, description=desc)
        newlist.save() 
        user.ownlists.add(newlist)
        user.save() 
    return HttpResponseRedirect(reverse('lists', args=[str(request.user.username)]))

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
        user.followingNum -= 1
        user2.followers -=1 
    else:
        user.following.add(FollowObj.objects.get(username=username))
        user.followingNum += 1
        user2.followers +=1 
        noti = Notification.objects.create(postUser = user, recieveUser = user2, text = user.username + " has started to follow you")
        noti.save() 
        user2.notificationlist.add(noti)
        user2.save()  
    user.save()
    user2.save() 
    return HttpResponseRedirect(reverse('profile', args=[str(username)]))

def Notifications(request):
    user = User2.objects.get(username=request.user.username)
    list = user.notificationlist.all() 
    haslist = True
    if len(list) == 0:
        haslist = False
    context = {"list": list, "haslist": haslist}
    return render(request, "twitter/notifications.html", context)

def Bookmark(request, pk):
    user = get_object_or_404(User2, username=request.user.username)
    post = get_object_or_404(Post, pk=pk)
    if user.bookmarks.filter(pk=post.pk).exists(): 
        user.bookmarks.remove(post)
    else:
        user.bookmarks.add(post)
    user.save() 
    return HttpResponseRedirect(reverse('post', args=[int(pk)]))

def Bookmarks(request):
    user = get_object_or_404(User2, username=request.user.username)
    bookmarklist = user.bookmarks.all().order_by("-pub_date"); full = True
    if len(bookmarklist) == 0:
        full = False
    context = {"bookmarklist": bookmarklist, "full": full}
    return render(request, 'twitter/bookmark.html', context)

def Lists(request, username):
    user = get_object_or_404(User2, username=request.user.username)
    listuser = get_object_or_404(User2, username=username)
    list = listuser.ownlists.all().order_by("name"); owned = True; own = False
    if len(list) == 0:
        owned = False 
    savedlist = user.savedlists.all().order_by("name"); saved = True
    if len(savedlist) == 0:
        saved = False
    if user.username == listuser.username:
        own = True
    context = {"lists": list, "owned": owned, "savedlist": savedlist, "saved": saved, "own": own, "username": username}
    return render(request, 'twitter/lists.html', context)

def List(request, pk):
    list = PostList.objects.get(pk=pk)
    own = False
    if list.user.username == request.user.username:
        own = True
    listlist = list.posts.all() 
    empty = False
    if len(listlist) == 0:
        empty = True
    saved = False
    if User2.objects.get(username=request.user.username).savedlists.filter(name=list.name).exists(): 
        saved = True
    context = {"list": list, "empty": empty, "listlist": listlist, "own": own, "saved": saved}
    return render(request, 'twitter/list.html', context)

def AddList(request, pk):
    user = get_object_or_404(User2, username=request.user.username)
    name = request.POST['list']
    if user.ownlists.filter(name=name).exists(): 
        list = user.ownlists.get(name=name)
        if not (list.posts.filter(pk=pk).exists()): 
            list.posts.add(Post.objects.get(pk=pk))
            list.numPosts += 1
            list.save() 
    return HttpResponseRedirect(reverse('post', args=[int(pk)]))

def DeleteList(request, pk):
    list = PostList.objects.get(pk=pk)
    if list.user.username == request.user.username: 
        list.delete() 
        return HttpResponseRedirect(reverse('lists', args=[str(request.user.username)]))
    else: 
        user = User2.objects.get(username=request.user.username)
        if user.savedlists.filter(pk=list.pk).exists():
            user.savedlists.remove(list)
        else: 
            user.savedlists.add(list)
        user.save() 
        return HttpResponseRedirect(reverse('list', args=[int(list.pk)]))

def Messages(request):
    user = get_object_or_404(User2, username=request.user.username)
    dms = MessageBoard.objects.filter(users__in=[user]).order_by("-last_messaged")
    empty = False
    if dms and len(dms) == 0:
        empty = True
    context = {"dms": dms, "empty": empty}
    return render(request, 'twitter/messages.html', context)

def Message(request, pk):
    dm = MessageBoard.objects.get(pk=pk)
    user = get_object_or_404(User2, username=request.user.username)
    messages = dm.messages.all().order_by("-time")
    if user in dm.users.all():
        context = {"dm": dm, "messages": messages}
        return render(request, 'twitter/message.html', context)
    return redirect('home')

def SendMessage(request, pk):
    dm = get_object_or_404(MessageBoard, pk=pk)
    message = MessageObj.objects.create(text=request.POST['message'], user=User2.objects.get(username=request.user.username), time=timezone.now())
    message.save()
    dm.messages.add(message)
    dm.last_messaged = timezone.now()
    dm.save()
    return redirect(Message, pk=pk)

def CreateMessage(request, usern):
    user1 = get_object_or_404(User2, username=request.user.username)
    user2 = get_object_or_404(User2, username=usern)
    dmcheck = MessageBoard.objects.filter(users__in=[user1, user2])
    valid = False
    for i in dmcheck:
        if user1 in i.users.all() and user2 in i.users.all():
            valid = True
    if valid:
        return redirect('messages')
    dm = MessageBoard.objects.create(name=str(user1) + " " + str(user2), last_messaged=timezone.now())
    dm.users.add(user1)
    dm.users.add(user2)
    dm.save()
    return redirect('messages')

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
                myfollow = FollowObj.objects.create(username=username)
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
