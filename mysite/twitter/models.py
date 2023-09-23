from django.db import models
from django.conf import settings
# Create your models here.

# figure out whether youre just gonna have each user be a text option in each post or if youre gonna have each user be its own object 
# dont wanna have to change that mid way through the process

class FollowObj(models.Model): #try and figure out if theres a better way to handle follows/friends for the discord project
    username = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class User2(models.Model): #don't delete follows or user2s manually, because you have to delete the user follow and user2 all in one or itll break
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200, default = "password")
    profile_picture = models.ImageField(upload_to = "media/twitter/", default = "static/twitter/default.png") 
    following = models.ManyToManyField(FollowObj, related_name="follow_account")
    bookmarks = models.ManyToManyField('Post', related_name="bookmarked_post") #if you want to define a relationship between two objects you can just use a string for the object name
    followers = models.IntegerField(default = 0)
    followingNum = models.IntegerField(default = 0)
    savedlists = models.ManyToManyField('PostList', related_name="saved_list")
    ownlists = models.ManyToManyField('PostList', related_name="own_list")
    posts = models.IntegerField(default = 0)
    notificationlist = models.ManyToManyField('Notification', related_name="notifications")
    def __str__(self):
        return self.username 

class MessageBoard(models.Model):
    user1= models.ForeignKey(User2, on_delete=models.PROTECT, related_name = "first")
    user2 = models.ForeignKey(User2, on_delete=models.PROTECT, related_name = "second")

class Message(models.Model):
    text = models.CharField(max_length=500)
<<<<<<< HEAD
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
=======
>>>>>>> 12fda536740ed293908f60a1802557df43eed78f
    board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE)

class Post(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User2, on_delete=models.PROTECT)
    likes = models.IntegerField(default = 0) 
    likedBy = models.ManyToManyField(User2, related_name="post_like")
    commentsCount = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.user) + " - " + self.text
    def getComments(self):
        return Comment.objects.filter(post = self)
    def likedByUser(self, username):
        return User2.objects.get(username=username) in self.likedBy 

class Notification(models.Model):
    # you probably couldve included something that says what the notification is notifying so that you could include links and the such but i didnt feel like it so boo hoo 
    postUser = models.ForeignKey(User2, on_delete = models.CASCADE, related_name="postuser")
    recieveUser = models.ForeignKey(User2, on_delete = models.CASCADE, related_name="recieveuser")
    text = models.CharField(max_length=200)
    link = models.CharField(max_length=200, default = "")

class PostList(models.Model): # make sure this name doesnt cause any errors, hopefully not
    posts = models.ManyToManyField(Post, related_name="listed_post")
    user = models.ForeignKey(User2, on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length = 200, default = "List")
    description = models.CharField(max_length = 200, default = "description...")
    numPosts = models.IntegerField(default=0) # figure out how to get length of the posts thing later for future models

class Comment(models.Model):
    text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    likes = models.IntegerField(default = 0)
    likedBy = models.ManyToManyField(User2, related_name="comment_like")
    comments = models.IntegerField(default = 0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " - " + self.text
    def getCommentsFix(self):
        return CommentUnderComment.objects.filter(post = self)

class CommentUnderComment(models.Model):
    text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User2, on_delete = models.CASCADE)
    likes = models.IntegerField(default = 0)
    likedBy = models.ManyToManyField(User2, related_name="commentplus_like")
    comments = models.IntegerField(default = 0)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " - " + self.text