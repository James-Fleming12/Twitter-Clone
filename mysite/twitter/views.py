from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.utils import timezone
from django.views import generic

class HomeView(generic.ListView):
    template_name = "twitter/home.html"
    context_object_name = "post_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

# def home(request):
#     return HttpResponse("Hello World, You're at the main screen")
