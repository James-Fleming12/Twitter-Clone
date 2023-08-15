from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView, name = "home"),
    path("user/<str:username>", views.ProfileView, name = "profile"),
    path("post/<int:pk>", views.PostView, name="post"),
    path("comment/<int:pk>", views.CommentView, name="comment"),
    path("login", views.LogIn, name = "login"),
    path("signup", views.SignUp, name = "signup"),
    path("signout", views.SignOut, name = "signout"),
    path("like/<int:pk>", views.PostLike, name="likepost"),
    path("likecomment/<int:pk>", views.CommentLike, name="likecomment"),
    path("delete/<int:pk>", views.DeletePost, name="deletepost"),
    path("deletecomment/<int:pk>", views.DeleteComment, name="deletecomment"),
    path("create", views.CreatePost, name="createpost"),
    path("follow/<str:username>", views.Follow, name="follow"),
    path("following", views.Following, name="following"),
    path("bookmark/<int:pk>", views.Bookmark, name="bookmark"),
    path("bookmarks", views.Bookmarks, name="bookmarks"),
    path("lists", views.Lists, name="lists")
    path("list/<int:pk>", views.List, name="list")
]