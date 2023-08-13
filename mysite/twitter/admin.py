from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(User2)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentUnderComment)
admin.site.register(FollowObj)
