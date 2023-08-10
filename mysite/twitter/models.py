from django.db import models

# Create your models here.

# figure out whether youre just gonna have each user be a text option in each post or if youre gonna have each user be its own object 
# dont wanna have to change that mid way through the process

class User2(models.Model): 
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200, default = "password")
    profile_picture = models.ImageField(upload_to = "media/twitter/", default = "static/twitter/default.png") 
    def __str__(self):
        return self.username 
    
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
    
class Comment(models.Model):
    text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    likes = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class CommentUnderComment(models.Model):
    text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User2, on_delete = models.CASCADE)
    likes = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)