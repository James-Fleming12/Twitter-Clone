from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView, name = "home"),
    path("user/<str:username>", views.ProfileView, name = "profile"),
    path("post/<int:pk>", views.PostView, name="post"),
    path("login", views.LogIn, name = "login"),
    path("signup", views.SignUp, name = "signup"),
    path("signout", views.SignOut, name = "signout"),
]