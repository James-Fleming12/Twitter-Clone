from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name = "home"),
    path("user/<str:username>", views.ProfileView, name = "profile"),
    path("post/<int:pk>", views.PostView, name="Post")
]