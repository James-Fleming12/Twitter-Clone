from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import *
from django.template import loader
from django.utils import timezone
from django.views import generic

class HomeView(generic.ListView):
    template_name = "twitter/home.html"
    context_object_name = "post_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

def ProfileView(request, username):
    tempUser = get_object_or_404(User, username=username)
    # post_list = loader(tempUser.post.objects.order_by("pub-date")[:5])
    post_list = Post.objects.filter(user = tempUser)
    context = {"post_list": post_list}
    return render(request, "twitter/profile.html", context)

def PostView(request, pk):
    tempPost = get_object_or_404(Post, pk=pk)
    context = {"post": tempPost}
    return render(request, 'twitter/post.html', context)

# def home(request):
#     return HttpResponse("Hello World, You're at the main screen")
